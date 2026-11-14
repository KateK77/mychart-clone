"""Password recovery with a browser-scoped, local-only simulated mailbox."""
import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST
from rest_framework import serializers as s
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser

from .auth import password_rules
from .models import PasswordReset
from .serializers import text, validated
from .services import atomic_change, audit

User = get_user_model()
GENERIC = "If an account matches that email, a password reset message has been sent."


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def limited(request, purpose, maximum=8):
    key = "auth-rate:" + purpose + ":" + digest(request.META.get("REMOTE_ADDR", "unknown"))
    if cache.add(key, 1, 600):
        return False
    return cache.incr(key) > maximum


def bad_input(exc):
    return JsonResponse({"detail": getattr(exc, "detail", "Check the information and try again.")}, status=400)


@require_POST
@atomic_change
def request_reset(request):
    if limited(request, "reset-request"):
        return JsonResponse({"detail": "Too many reset requests. Please try again in 10 minutes."}, status=429)
    try:
        data = validated(JSONParser().parse(request), email=s.EmailField())
    except Exception as exc:
        return bad_input(exc)
    # Only demo mode delivers messages locally. Production requires a configured mail service.
    if not settings.DEMO_MAILBOX:
        return JsonResponse({"detail": "Password recovery is not configured. Please contact support."}, status=503)
    matches = list(User.objects.select_for_update().filter(email__iexact=data["email"], is_active=True)[:2])
    if len(matches) == 1 and matches[0].has_usable_password():
        user = matches[0]
        token = secrets.token_urlsafe(32)
        expires = timezone.now() + timedelta(minutes=30)
        PasswordReset.objects.filter(user=user, used_at__isnull=True).update(used_at=timezone.now())
        PasswordReset.objects.create(user=user, token_hash=digest(token),
                                     password_fingerprint=digest(user.password), expires_at=expires)
        # Messages are held in this browser's server-side session, never in a public global inbox.
        messages = request.session.get("demo_mail", [])
        messages.insert(0, {"id": secrets.token_hex(8), "to": user.email,
            "subject": "Reset your CareConnect password", "created_at": timezone.now().isoformat(),
            "expires_at": expires.isoformat(), "link": "/reset-password?token=" + token,
            "body": "A password reset was requested for your CareConnect account. This link expires in 30 minutes and can be used once. If you did not request this, you can ignore this message."})
        request.session["demo_mail"] = messages[:5]
        audit(user, "Password reset requested", getattr(user, "patient", None))
    return JsonResponse({"detail": GENERIC})


@require_GET
def mailbox(request):
    if not settings.DEMO_MAILBOX:
        raise Http404
    return JsonResponse({"messages": request.session.get("demo_mail", [])})


@require_POST
@atomic_change
def reset_password(request):
    if limited(request, "reset-submit", 15):
        return JsonResponse({"detail": "Too many attempts. Please try again in 10 minutes."}, status=429)
    try:
        data = validated(JSONParser().parse(request), token=text(length=160),
                         password=text(length=128), confirm_password=text(length=128))
        if data["password"] != data["confirm_password"]:
            raise ValidationError("The new passwords do not match.")
        record = PasswordReset.objects.select_for_update().filter(token_hash=digest(data["token"])).first()
        if not record or record.used_at or record.expires_at <= timezone.now():
            raise ValidationError("This reset link has expired or has already been used. Request a new link.")
        user = User.objects.select_for_update().get(pk=record.user_id)
        if not user.is_active or digest(user.password) != record.password_fingerprint:
            raise ValidationError("This reset link is no longer valid. Request a new link.")
        password_rules(data["password"], user)
    except Exception as exc:
        return bad_input(exc)
    user.set_password(data["password"])
    user.save(update_fields=["password"])
    PasswordReset.objects.filter(user=user, used_at__isnull=True).update(used_at=timezone.now())
    audit(user, "Password reset completed", getattr(user, "patient", None))
    # Existing authenticated sessions become invalid through Django's session auth hash.
    return JsonResponse({"detail": "Your password has been reset. Sign in with your new password."})
