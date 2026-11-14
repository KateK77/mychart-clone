from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, OperationalError, transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from . import models as m

CLINICAL = ("Physician", "Nurse")
SCHEDULING = ("Front Desk", *CLINICAL)
BILLING = ("Billing Staff",)
TEAMS = {"Care team": CLINICAL, "Scheduling": SCHEDULING, "Billing": BILLING}


def roles(user):
    return set(user.groups.values_list("name", flat=True))


def require_staff(user, allowed):
    if not roles(user).intersection((*allowed, "Administrator")):
        raise PermissionDenied


def audit(actor, action, patient=None, target=""):
    m.AuditEvent.objects.create(actor=actor, patient=patient, action=action, target=str(target))


def notify(patient, kind, title, destination):
    if kind not in patient.muted_notifications:
        m.Notification.objects.create(patient=patient, kind=kind, title=title, destination=destination)


def patient_scope(request, section):
    user = request.user
    own = getattr(user, "patient", None)
    requested = request.query_params.get("patient")
    if not requested or (own and requested == str(own.pk)):
        if own:
            return own
        raise PermissionDenied
    if not requested.isdigit():
        raise PermissionDenied("This family profile is not available to your account.")
    grant = m.ProxyAccess.objects.select_related("patient").filter(proxy=user, patient_id=requested, active=True).first()
    if not grant:
        raise PermissionDenied("Access to this family profile is no longer available. Choose another profile from Family Access.")
    if section not in grant.sections:
        raise PermissionDenied("This part of the family profile has not been shared with you. Choose a permitted section from Family Access.")
    return grant.patient


def read_audit(request, patient, section, target=""):
    audit(request.user, f"Read {section}", patient, target)


def atomic_change(fn):
    from functools import wraps

    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            with transaction.atomic():
                return fn(*args, **kwargs)
        except IntegrityError as exc:
            raise ValidationError("The change conflicts with an existing record.") from exc
        except OperationalError as exc:
            if "locked" not in str(exc).lower():
                raise
            raise ValidationError("Another change is in progress. Please try again.") from exc

    return wrapped


APPOINTMENT_TRANSITIONS = {
    "Scheduled": ("Confirmed", "Checked In", "Cancelled", "No Show"),
    "Confirmed": ("Checked In", "Cancelled", "No Show"),
    "Checked In": ("Completed", "Cancelled"),
}
REFILL_TRANSITIONS = {
    "Requested": ("Under Review", "Approved", "Denied"),
    "Under Review": ("Approved", "Denied"),
    "Approved": ("Completed",),
}


def available_slots():
    return m.Slot.objects.filter(active=True, provider__active=True, starts_at__gt=timezone.now()).exclude(
        pk__in=m.Appointment.objects.exclude(status="Cancelled").values("slot_id")
    ).select_related("provider__department").order_by("starts_at")


def book(user, patient, slot_id, predecessor=None):
    slot = get_object_or_404(available_slots().select_for_update(of=("self",)), pk=slot_id)
    appointment = m.Appointment.objects.create(patient=patient, slot=slot, predecessor=predecessor)
    audit(user, "Appointment booked", patient, appointment.pk)
    notify(patient, "Appointment", "Appointment scheduled", f"/appointments/{appointment.pk}")
    return appointment


def change_appointment(user, appointment, state, reason=""):
    if state not in APPOINTMENT_TRANSITIONS.get(appointment.status, ()):
        raise ValidationError("This appointment cannot move to the selected status.")
    if state == "Cancelled" and not reason:
        raise ValidationError("Enter a cancellation reason.")
    appointment.status = state
    appointment.cancellation_reason = reason if state == "Cancelled" else ""
    appointment.save()
    audit(user, f"Appointment {state}", appointment.patient, appointment.pk)
    if state == "Cancelled":
        notify(appointment.patient, "Cancellation", "Appointment cancelled", f"/appointments/{appointment.pk}")


def pay(user, invoice, amount, key):
    existing = m.Payment.objects.filter(actor=user, request_key=key).first()
    if existing:
        if existing.invoice_id != invoice.pk or existing.amount != amount:
            raise ValidationError("This payment reference was already used.")
        return existing
    if amount > invoice.balance:
        raise ValidationError("Amount exceeds the outstanding balance.")
    payment = m.Payment.objects.create(invoice=invoice, actor=user, request_key=key, amount=amount)
    invoice.paid += amount
    invoice.save(update_fields=["paid"])
    audit(user, "Payment recorded", invoice.patient, payment.pk)
    notify(invoice.patient, "Payment", "Simulated payment recorded", f"/billing/{invoice.pk}")
    return payment
