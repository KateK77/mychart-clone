from decimal import Decimal

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers as s
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from . import models as m
from .serializers import fields_for, serialize, text, validated, select
from .services import BILLING, CLINICAL, SCHEDULING, REFILL_TRANSITIONS, atomic_change, audit, book, change_appointment, notify, pay, require_staff

RESOURCES = {
    "departments": (m.Department, SCHEDULING, ()),
    "providers": (m.Provider, SCHEDULING, ()),
    "slots": (m.Slot, SCHEDULING, ()),
    "appointments": (m.Appointment, SCHEDULING, ()),
    "results": (m.LabResult, CLINICAL, ("published",)),
    "medications": (m.Medication, CLINICAL, ()),
    "refills": (m.Refill, CLINICAL, ()),
    "health": (m.HealthEntry, CLINICAL, ()),
    "reports": (m.Report, CLINICAL, ("patient", "topic", "details")),
    "visits": (m.Encounter, CLINICAL, ("published",)),
    "diagnoses": (m.Diagnosis, CLINICAL, ()),
    "notes": (m.ClinicalNote, CLINICAL, ()),
    "billing": (m.Invoice, BILLING, ()),
    "insurance": (m.Insurance, BILLING, ()),
    "documents": (m.Document, CLINICAL, ("published",)),
    "proxy": (m.ProxyAccess, (), ()),
}


@api_view(["GET"])
def patients(request):
    require_staff(request.user, (*SCHEDULING, *BILLING))
    query = request.query_params.get("q", "")[:150]
    rows = m.Patient.objects.select_related("user").filter(
        Q(user__username__icontains=query) | Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query)
    ).order_by("user__last_name")
    audit(request.user, "Staff searched patients")
    return Response([{"id": row.pk, "name": str(row), "user": row.user_id, "username": row.user.username} for row in rows[:100]])


def record_patient(row):
    if isinstance(row, m.Refill):
        return row.medication.patient
    if isinstance(row, (m.Diagnosis, m.ClinicalNote)):
        return row.encounter.patient
    return getattr(row, "patient", None)


def update_special(request, resource, row):
    user, incoming = request.user, request.data
    patient = record_patient(row)
    if resource == "appointments":
        data = validated(incoming, action=select(("status", "reschedule")), status=s.ChoiceField(choices=m.APPOINTMENT_STATES, required=False),
                         note=text(False), slot=s.IntegerField(required=False, min_value=1))
        if data["action"] == "reschedule" and data.get("slot"):
            if row.status not in ("Scheduled", "Confirmed") or row.starts_at <= timezone.now():
                raise ValidationError("Only upcoming scheduled appointments can be rescheduled.")
            change_appointment(user, row, "Cancelled", data.get("note") or "Rescheduled by staff")
            return Response(serialize(book(user, patient, data["slot"], row)))
        change_appointment(user, row, data.get("status"), data.get("note", ""))
    elif resource == "refills":
        data = validated(incoming, status=select(m.REFILL_STATES), decision=text(False))
        state = data["status"]
        if state not in REFILL_TRANSITIONS.get(row.status, ()):
            raise ValidationError("This refill cannot move to the selected status.")
        row.status, row.decision = state, data.get("decision", "")
        row.save(update_fields=["status", "decision"])
        audit(user, f"Refill {state}", patient, row.pk)
        notify(patient, "Refill", f"Refill {state.lower()}", f"/medications/{row.medication_id}")
    elif resource == "billing":
        data = validated(incoming, amount=s.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0.01")), key=s.UUIDField())
        return Response(serialize(pay(user, row, data["amount"], data["key"])), status=201)
    elif resource in ("results", "visits", "documents"):
        data = validated(incoming, published=s.BooleanField())
        changed = row.published != data["published"]
        row.published = data["published"]
        row.save(update_fields=["published"])
        audit(user, f"{resource.title()} publication changed", patient, row.pk)
        if changed and resource == "results" and row.published:
            notify(patient, "Test result", f"New result · {row.name}", f"/results/{row.pk}")
    else:
        raise ValidationError("Unsupported operation.")
    return Response(serialize(row))


@api_view(["GET", "POST", "PATCH"])
@atomic_change
def records(request, resource, pk=None):
    if resource not in RESOURCES:
        from django.http import Http404
        raise Http404
    model, allowed, readonly = RESOURCES[resource]
    require_staff(request.user, allowed)
    qs = model.objects.all()
    patient_id = request.query_params.get("patient")
    if patient_id:
        allowed_filter = ("medication__patient_id" if model is m.Refill else "encounter__patient_id"
                          if model in (m.Diagnosis, m.ClinicalNote) else "patient_id"
                          if issubclass(model, m.PatientRecord) else None)
        if allowed_filter:
            try:
                patient_id = int(patient_id)
            except ValueError as exc:
                raise ValidationError("Invalid patient identifier.") from exc
            qs = qs.filter(**{allowed_filter: patient_id})
    row = get_object_or_404(qs.select_for_update() if request.method != "GET" else qs, pk=pk) if pk else None
    if request.method == "GET":
        audit(request.user, f"Staff read {resource}", record_patient(row), pk or patient_id or "")
        return Response(serialize(row) if row else [serialize(item) for item in qs.order_by("-pk")[:150]])
    if request.method == "POST" and pk:
        return update_special(request, resource, row)
    if request.method == "PATCH" and not pk:
        raise ValidationError("Select a record to update.")
    if model is m.Appointment:
        if row:
            raise ValidationError("Use an appointment action to update its status.")
        data = validated(request.data, slot=s.IntegerField(min_value=1), patient=s.IntegerField(min_value=1))
        patient = get_object_or_404(m.Patient, pk=data["patient"])
        return Response(serialize(book(request.user, patient, data["slot"])), status=201)
    if model is m.Refill or (model is m.Report and not row):
        raise ValidationError("This record is created through the patient portal.")
    if model is m.ProxyAccess:
        data = validated(request.data, patient=s.IntegerField(min_value=1, required=not row),
                         proxy=s.IntegerField(min_value=1, required=not row),
                         active=s.BooleanField(required=False),
                         sections=s.ListField(child=select(m.PROXY_SECTIONS), allow_empty=False, required=not row))
        from django.contrib.auth import get_user_model
        if row and ("patient" in data or "proxy" in data):
            raise ValidationError("Patient and proxy cannot be reassigned.")
        patient = row.patient if row else get_object_or_404(m.Patient, pk=data.pop("patient"))
        if not row:
            proxy = get_object_or_404(get_user_model(), pk=data.pop("proxy"), patient__isnull=False)
            if proxy.id == patient.user_id:
                raise ValidationError("Select a different patient account as proxy.")
            row, _ = model.objects.update_or_create(patient=patient, proxy=proxy, defaults={"active": True, **data})
        else:
            for key, value in data.items():
                setattr(row, key, value)
            row.save()
    else:
        readonly = (*readonly, "patient") if row and issubclass(model, m.PatientRecord) else readonly
        if row and model in (m.Diagnosis, m.ClinicalNote):
            readonly = (*readonly, "encounter")
        form = fields_for(model, readonly=readonly)(row, data=request.data, partial=bool(row))
        form.is_valid(raise_exception=True)
        row = form.save()
        patient = record_patient(row)
    audit(request.user, f"Staff changed {resource}", patient, row.pk)
    if resource == "billing" and request.method == "POST":
        notify(patient, "Billing statement", "New billing statement", f"/billing/{row.pk}")
    return Response(serialize(row), status=200 if pk else 201)
