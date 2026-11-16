from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers as s
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from . import models as m
from .services import atomic_change, audit, require_staff
from .serializers import validated, text

User = get_user_model()


def bind_invitations(user):
    # Bind only during registration, never after a profile email change.
    m.FamilyRequest.objects.filter(recipient__isnull=True, recipient_email__iexact=user.email).update(recipient=user)


def name(user):
    return user.get_full_name() or user.username


def sections_field(required=True):
    return s.ListField(child=s.ChoiceField(choices=m.PROXY_SECTIONS), allow_empty=False, required=required, max_length=7)


def minor(patient):
    today = timezone.localdate()
    birth = patient.birth_date
    return bool(birth and today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day)) < 18)


def request_data(row, user):
    status = "Expired" if row.status in ("Pending", "Awaiting review") and row.expires_at <= timezone.now() else row.status
    return {"id": row.pk, "from_name": name(row.requester), "to_email": row.recipient_email,
            "direction": row.direction, "relationship": row.relationship, "sections": row.sections,
            "status": status, "decision": row.decision, "expires_at": row.expires_at,
            "incoming": row.recipient_id == user.pk, "outgoing": row.requester_id == user.pk}


def activate(row, actor):
    if row.direction == "Invite":
        owner, proxy = row.owner, row.recipient
    else:
        owner, proxy = getattr(row.recipient, "patient", None), row.requester
    if not owner or not getattr(proxy, "patient", None):
        raise ValidationError("Both people need a patient or family caregiver account before access can be linked.")
    if owner.user_id == proxy.pk:
        raise ValidationError("Choose a different family member.")
    grant, _ = m.ProxyAccess.objects.get_or_create(patient=owner, proxy=proxy, defaults={"sections": [], "active": False})
    grant.sections = sorted(set((grant.sections if grant.active else []) + row.sections))
    grant.active = True
    grant.save()
    row.owner, row.status = owner, "Accepted"
    row.save()
    audit(actor, "Family access accepted", owner, grant.pk)


@api_view(["GET", "POST"])
@atomic_change
def family_requests(request, pk=None):
    user = request.user
    own = getattr(user, "patient", None)
    if not own:
        raise PermissionDenied
    if request.method == "GET":
        requests = m.FamilyRequest.objects.filter(Q(requester=user) | Q(recipient=user)).select_related("requester").order_by("-pk")
        shared = m.ProxyAccess.objects.filter(patient=own).select_related("proxy")
        linked = m.ProxyAccess.objects.filter(proxy=user, active=True).select_related("patient__user")
        return Response({"requests": [request_data(row, user) for row in requests], "sections": list(m.PROXY_SECTIONS),
                         "linked": [{"id": row.pk, "patient": row.patient_id, "name": str(row.patient), "sections": row.sections} for row in linked],
                         "shared": [{"id": row.pk, "name": name(row.proxy), "sections": row.sections, "active": row.active} for row in shared]})
    if pk:
        row = get_object_or_404(m.FamilyRequest.objects.select_for_update().filter(Q(requester=user) | Q(recipient=user)), pk=pk)
        data = validated(request.data, action=s.ChoiceField(choices=("accept", "decline", "cancel")))
        if row.status not in ("Pending", "Awaiting review") or row.expires_at <= timezone.now():
            raise ValidationError("This request is no longer pending. Create a new invitation if needed.")
        action = data["action"]
        if action == "cancel":
            if row.requester_id != user.pk:
                raise PermissionDenied
            row.status = "Cancelled"
        else:
            if row.recipient_id != user.pk:
                raise PermissionDenied
            if action == "accept":
                if row.status == "Awaiting review" or minor(own) or (row.owner and minor(row.owner)):
                    raise ValidationError("Guardian access requires administrator review before it can be granted.")
                activate(row, user)
            else:
                row.status = "Declined"
        row.save()
        audit(user, "Family request " + row.status, row.owner, row.pk)
        return Response(request_data(row, user))
    data = validated(request.data, email=s.EmailField(), direction=s.ChoiceField(choices=("Invite", "Request", "Guardian")),
                     relationship=text(length=100), sections=sections_field())
    if data["email"].casefold() == user.email.casefold():
        raise ValidationError("Enter your family member's email, rather than your own.")
    recipient = User.objects.filter(email__iexact=data["email"]).first()
    if recipient and not hasattr(recipient, "patient"):
        raise ValidationError("Family linking requires a patient or family caregiver account.")
    direction = data["direction"]
    target = own if direction == "Invite" else getattr(recipient, "patient", None)
    review = direction == "Guardian" or (target and minor(target))
    if m.FamilyRequest.objects.filter(requester=user, recipient_email__iexact=data["email"], direction=direction,
                                     status__in=("Pending", "Awaiting review"), expires_at__gt=timezone.now()).exists():
        raise ValidationError("There is already a pending request for this person. View it below.")
    row = m.FamilyRequest.objects.create(requester=user, recipient=recipient, recipient_email=data["email"].lower(),
        owner=own if direction == "Invite" else None, direction=direction, relationship=data["relationship"],
        sections=sorted(set(data["sections"])), status="Awaiting review" if review else "Pending", expires_at=timezone.now()+timedelta(days=14))
    audit(user, "Family request created", own, row.pk)
    return Response(request_data(row, user), status=201)


@api_view(["POST"])
@atomic_change
def revoke(request, pk):
    own = getattr(request.user, "patient", None)
    row = get_object_or_404(m.ProxyAccess.objects.select_for_update().filter(Q(patient=own) | Q(proxy=request.user)), pk=pk)
    row.active = False
    row.save(update_fields=["active"])
    # An older pending invitation cannot silently restore revoked access.
    m.FamilyRequest.objects.filter(status__in=("Pending", "Awaiting review")).filter(
        Q(requester=row.patient.user, recipient=row.proxy) | Q(requester=row.proxy, recipient=row.patient.user)).update(status="Cancelled")
    audit(request.user, "Family access revoked", row.patient, row.pk)
    return Response({"detail": "Family access revoked. A new consent request is needed to link again."})


@api_view(["GET", "POST"])
@atomic_change
def reviews(request, kind=None, pk=None):
    require_staff(request.user, ())  # Administrator only; care-team roles cannot grant roles.
    if request.method == "GET":
        return Response({"staff": [{"id": r.pk, "name": name(r.user), "email": r.user.email, "role": r.requested_role,
            "organization": r.organization, "reason": r.reason, "status": r.status, "decision": r.decision}
            for r in m.StaffApplication.objects.select_related("user").order_by("-pk")],
            "guardian": [request_data(r, request.user) for r in m.FamilyRequest.objects.filter(status="Awaiting review").select_related("requester")]})
    data = validated(request.data, action=s.ChoiceField(choices=("approve", "decline")), decision=text())
    if kind == "staff":
        row = get_object_or_404(m.StaffApplication.objects.select_for_update(), pk=pk, status="Pending")
        row.status = "Approved" if data["action"] == "approve" else "Declined"
        row.decision, row.reviewer = data["decision"], request.user
        row.save()
        if row.status == "Approved":
            group, _ = Group.objects.get_or_create(name=row.requested_role)
            row.user.groups.add(group)
        audit(request.user, "Staff application " + row.status, target=row.pk)
    elif kind == "guardian":
        row = get_object_or_404(m.FamilyRequest.objects.select_for_update(), pk=pk, status="Awaiting review")
        if row.expires_at <= timezone.now():
            raise ValidationError("This request has expired.")
        if data["action"] == "approve":
            activate(row, request.user)
        else:
            row.status = "Declined"
        row.decision = data["decision"]
        row.save()
        audit(request.user, "Guardian request " + row.status, row.owner, row.pk)
    else:
        raise ValidationError("Unknown review type.")
    return Response({"detail": "Review saved."})
