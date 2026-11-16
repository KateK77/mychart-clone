from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from rest_framework import serializers as s
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from . import models as m
from .serializers import text, validated
from .services import atomic_change, audit, roles

User = get_user_model()


def identity(user):
    patient = getattr(user, "patient", None)
    return {"id": user.pk, "name": user.get_full_name() or user.username,
            "roles": sorted(roles(user)) or (["Patient"] if patient else []), "patient": patient.pk if patient else None,
            "account_kind": patient.account_kind if patient else "Care team",
            "application": ({"status": user.staff_application.status, "role": user.staff_application.requested_role,
                             "decision": user.staff_application.decision} if hasattr(user, "staff_application") else None)}


@ensure_csrf_cookie
def session(request):
    return JsonResponse({"user": identity(request.user) if request.user.is_authenticated else None, "demo_mailbox": settings.DEMO_MAILBOX})


@require_POST
def sign_in(request):
    try:
        data = validated(JSONParser().parse(request), username=text(length=150), password=text(length=128))
    except Exception:
        return JsonResponse({"detail": "Enter a valid username and password."}, status=400)
    user = authenticate(request, **data)
    if not user:
        return JsonResponse({"detail": "Invalid username or password."}, status=400)
    login(request, user)
    audit(user, "Login", getattr(user, "patient", None))
    return JsonResponse({"user": identity(user)})


@require_POST
def sign_out(request):
    logout(request)
    return JsonResponse({"user": None})


def password_rules(password, user):
    try:
        validate_password(password, user)
    except DjangoValidationError as exc:
        raise ValidationError({"password": exc.messages}) from exc


@require_POST
@atomic_change
def register(request):
    try:
        data = validated(JSONParser().parse(request), username=s.RegexField(r"^[a-zA-Z0-9_.-]+$", max_length=150),
                         first_name=text(length=150), last_name=text(length=150), email=s.EmailField(), password=text(length=128), confirm_password=text(length=128),
                         account_type=s.ChoiceField(choices=("patient", "caregiver", "careteam"), default="patient"),
                         requested_role=s.ChoiceField(choices=m.ROLES[:-1], required=False), organization=text(False, 150), reason=text(False))
        password = data.pop("password")
        if data.pop("confirm_password") != password:
            raise ValidationError("The new passwords do not match.")
        account_type = data.pop("account_type")
        requested_role, organization, reason = data.pop("requested_role", ""), data.pop("organization", ""), data.pop("reason", "")
        if account_type == "careteam" and (not requested_role or not organization):
            raise ValidationError("Select your care-team role and enter your organization.")
        user = User(**data)
        password_rules(password, user)
    except Exception as exc:
        return JsonResponse({"detail": getattr(exc, "detail", "Check the account details.")}, status=400)
    if User.objects.filter(username=user.username).exists():
        return JsonResponse({"detail": "This username is already in use."}, status=400)
    if User.objects.filter(email__iexact=user.email).exists():
        return JsonResponse({"detail": "This email is already associated with another account."}, status=400)
    user.set_password(password)
    from django.db import IntegrityError, transaction
    try:
        with transaction.atomic():
            user.save()
            if account_type == "careteam":
                m.StaffApplication.objects.create(user=user, requested_role=requested_role, organization=organization, reason=reason)
            else:
                m.Patient.objects.create(user=user, account_kind="Caregiver" if account_type == "caregiver" else "Patient")
    except IntegrityError:
        return JsonResponse({"detail": "This username is already in use."}, status=409)
    from .access import bind_invitations
    bind_invitations(user)
    login(request, user)
    audit(user, "Registration", getattr(user, "patient", None))
    return JsonResponse({"user": identity(user)}, status=201)


@api_view(["GET", "PATCH"])
@atomic_change
def profile(request):
    user = request.user
    patient = getattr(user, "patient", None)
    if request.method == "PATCH":
        data = validated(request.data, email=s.EmailField(required=False), phone=text(False, 40),
                         address=text(False, 240), birth_date=s.DateField(required=False, allow_null=True),
                         muted_notifications=s.ListField(child=s.ChoiceField(choices=m.EVENT_TYPES), required=False))
        if "email" in data:
            if User.objects.filter(email__iexact=data["email"]).exclude(pk=user.pk).exists():
                raise ValidationError("This email is already associated with another account.")
            user.email = data.pop("email")
            user.save(update_fields=["email"])
        if data and patient:
            for field, value in data.items():
                setattr(patient, field, value)
            patient.save(update_fields=data.keys())
        audit(user, "Profile updated", patient)
    return Response({**identity(user), "email": user.email, "phone": patient.phone if patient else "",
                     "address": patient.address if patient else "", "birth_date": patient.birth_date if patient else None,
                     "muted_notifications": patient.muted_notifications if patient else [], "notification_types": m.EVENT_TYPES})


@api_view(["POST"])
def password(request):
    data = validated(request.data, current=text(length=128), password=text(length=128), confirm_password=text(length=128))
    user = request.user
    if not user.check_password(data["current"]):
        raise ValidationError("Current password is incorrect.")
    if data["password"] != data["confirm_password"]:
        raise ValidationError("The new passwords do not match.")
    password_rules(data["password"], user)
    user.set_password(data["password"])
    user.save(update_fields=["password"])
    update_session_auth_hash(request, user)
    audit(user, "Password changed", getattr(user, "patient", None))
    return Response({"detail": "Password changed."})
