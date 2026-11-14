from decimal import Decimal

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers as s
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from . import models as m
from .serializers import serialize, text, validated, select
from .services import atomic_change, audit, available_slots, book, change_appointment, notify, patient_scope, pay, read_audit


def listing(rows, exclude=()):
    return [serialize(row, exclude) for row in rows]


def download(content, filename, inline=False):
    response = HttpResponse(content, content_type="text/plain; charset=utf-8")
    response["Content-Disposition"] = f'{"inline" if inline else "attachment"}; filename="{filename}"'
    response["Cache-Control"] = "private, no-store"
    return response


@api_view(["GET"])
def dashboard(request):
    patient = patient_scope(request, "dashboard")
    read_audit(request, patient, "dashboard")
    now = timezone.now()
    upcoming = m.Appointment.objects.filter(patient=patient, starts_at__gte=now, status__in=("Scheduled", "Confirmed", "Checked In"))
    unread = m.Message.objects.filter(thread__patient=patient).exclude(sender=request.user).exclude(read_by=request.user)
    return Response({
        "name": str(patient), "appointments": listing(upcoming.order_by("starts_at")[:3]),
        "results": listing(m.LabResult.objects.filter(patient=patient, published=True).order_by("-collected_at", "-pk")[:4]),
        "medications": listing(m.Medication.objects.filter(patient=patient, status="Active").order_by("name")[:4]),
        "visits": listing(m.Encounter.objects.filter(patient=patient, published=True).order_by("-date")[:3]),
        "notifications": listing(patient.notification_set.order_by("-pk")[:5]),
        "unread": unread.count(), "balance": str(sum((row.balance for row in patient.invoice_set.all()), Decimal("0.00"))),
    })


@api_view(["GET", "POST"])
@atomic_change
def appointments(request, pk=None):
    patient = patient_scope(request, "appointments")
    rows = m.Appointment.objects.filter(patient=patient).select_related("slot__provider__department")
    if request.method == "GET":
        read_audit(request, patient, "appointments", pk or "")
        return Response(serialize(get_object_or_404(rows, pk=pk)) if pk else listing(rows.order_by("-starts_at")))
    if not pk:
        data = validated(request.data, slot=s.IntegerField(min_value=1))
        return Response(serialize(book(request.user, patient, data["slot"])), status=201)
    row = get_object_or_404(rows.select_for_update(of=("self",)), pk=pk)
    data = validated(request.data, action=select(("cancel", "reschedule", "questionnaire", "check-in")), note=text(False))
    action, note = data["action"], data.get("note", "")
    if row.starts_at <= timezone.now() or row.status not in ("Scheduled", "Confirmed"):
        raise ValidationError("This action requires an upcoming scheduled or confirmed appointment.")
    if action == "cancel":
        change_appointment(request.user, row, "Cancelled", note)
    elif action == "check-in":
        if not row.questionnaire:
            raise ValidationError("Complete the pre-visit questionnaire before checking in.")
        change_appointment(request.user, row, "Checked In")
    elif action == "reschedule" and note:
        row.reschedule_requested = True
        row.reschedule_reason = note
        row.save(update_fields=["reschedule_requested", "reschedule_reason"])
        audit(request.user, "Reschedule requested", patient, row.pk)
    elif action == "questionnaire" and note:
        row.questionnaire = note
        row.save(update_fields=["questionnaire"])
        audit(request.user, "Questionnaire saved", patient, row.pk)
    else:
        raise ValidationError("Enter the requested information.")
    return Response(serialize(row))


@api_view(["GET"])
def slots(request):
    patient_scope(request, "appointments")
    args = validated({key: value for key, value in request.query_params.items() if key != "patient"}, provider=s.IntegerField(required=False, min_value=1),
                     kind=s.ChoiceField(choices=m.APPOINTMENT_TYPES, required=False),
                     date=s.DateField(required=False))
    if "date" in args:
        args["starts_at__date"] = args.pop("date")
    return Response({"slots": listing(available_slots().filter(**args)[:150]),
                     "providers": listing(m.Provider.objects.filter(active=True).order_by("name")),
                     "types": m.APPOINTMENT_TYPES})


@api_view(["GET"])
def results(request, pk=None, file=False):
    patient = patient_scope(request, "results")
    rows = m.LabResult.objects.filter(patient=patient, published=True).select_related("provider__department")
    read_audit(request, patient, "results", pk or "")
    if pk:
        row = get_object_or_404(rows, pk=pk)
        record = serialize(row)
        if file:
            keys = ("name", "collected_at", "resulted_at", "value", "unit", "reference_low", "reference_high", "flag", "status", "provider_name", "comments")
            report = "\n".join(f"{key.replace('_', ' ').title()}: {record[key] if record[key] is not None else ''}" for key in keys)
            return download("CareConnect · Synthetic laboratory report\n\n" + report, f"lab-{pk}.txt")
        record["history"] = listing(rows.filter(name__iexact=row.name, unit=row.unit, value__isnull=False).order_by("collected_at", "pk"))
        return Response(record)
    args = validated(request.query_params, patient=s.IntegerField(required=False),
                     q=text(False, 120), after=s.DateField(required=False), before=s.DateField(required=False))
    if args.get("q"):
        rows = rows.filter(name__icontains=args["q"])
    if args.get("after"):
        rows = rows.filter(collected_at__gte=args["after"])
    if args.get("before"):
        rows = rows.filter(collected_at__lte=args["before"])
    return Response(listing(rows.order_by("-collected_at", "-pk")))


@api_view(["GET", "POST"])
@atomic_change
def medications(request, pk=None):
    patient = patient_scope(request, "medications")
    rows = m.Medication.objects.filter(patient=patient).select_related("provider__department")
    refills = m.Refill.objects.filter(medication__patient=patient).select_related("medication").order_by("-pk")
    if request.method == "POST":
        row = get_object_or_404(rows.select_for_update(of=("self",)), pk=pk)
        data = validated(request.data, note=text(False))
        today = timezone.localdate()
        if row.status != "Active" or row.start_date > today or (row.end_date and row.end_date < today):
            raise ValidationError("Refills require a current medication.")
        refill = m.Refill.objects.create(medication=row, note=data.get("note", ""))
        audit(request.user, "Refill requested", patient, refill.pk)
        return Response(serialize(refill), status=201)
    read_audit(request, patient, "medications", pk or "")
    if pk:
        return Response({**serialize(get_object_or_404(rows, pk=pk)), "refills": listing(refills.filter(medication_id=pk))})
    query = request.query_params.get("q", "")[:120]
    return Response({"medications": listing(rows.filter(name__icontains=query).order_by("name")), "refills": listing(refills)})


@api_view(["POST"])
def report(request):
    data = validated(request.data, topic=select(("Medication", "Health summary")), details=text())
    patient = patient_scope(request, "medications" if data["topic"] == "Medication" else "health")
    row = m.Report.objects.create(patient=patient, **data)
    audit(request.user, "Patient reported update", patient, row.pk)
    return Response(serialize(row), status=201)


@api_view(["GET"])
def health(request):
    patient = patient_scope(request, "health")
    read_audit(request, patient, "health")
    return Response({"demographics": {"name": str(patient), "birth_date": patient.birth_date, "phone": patient.phone, "address": patient.address},
                     "sections": {section: listing(patient.healthentry_set.filter(section=section).order_by("-date", "title")) for section in m.HEALTH_TYPES},
                     "medications": listing(patient.medication_set.filter(status="Active"))})


@api_view(["GET"])
def visits(request, pk=None):
    patient = patient_scope(request, "visits")
    read_audit(request, patient, "visits", pk or "")
    rows = patient.encounter_set.filter(published=True).select_related("provider__department")
    if not pk:
        return Response(listing(rows.order_by("-date"), ("summary", "follow_up")))
    row = get_object_or_404(rows, pk=pk)
    return Response({**serialize(row), "diagnoses": listing(row.diagnoses.all()), "notes": listing(row.notes.filter(shared=True)),
                     "documents": listing(row.document_set.filter(patient=patient, published=True, kind="After Visit Summary"), ("content",))})


@api_view(["GET", "POST"])
@atomic_change
def billing(request, pk=None):
    patient = patient_scope(request, "billing")
    rows = patient.invoice_set.all()
    if request.method == "POST":
        data = validated(request.data, amount=s.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0.01")), key=s.UUIDField())
        row = get_object_or_404(rows.select_for_update(), pk=pk)
        return Response(serialize(pay(request.user, row, data["amount"], data["key"])), status=201)
    read_audit(request, patient, "billing", pk or "")
    payments = m.Payment.objects.filter(invoice__patient=patient).order_by("-pk")
    if pk:
        return Response({**serialize(get_object_or_404(rows, pk=pk)), "payments": listing(payments.filter(invoice_id=pk), ("request_key",))})
    return Response({"invoices": listing(rows.order_by("-service_date")), "payments": listing(payments, ("request_key",)),
                     "insurance": listing(patient.insurance_set.all()), "balance": str(sum((row.balance for row in rows), Decimal("0.00")))})


@api_view(["GET"])
def receipt(request, pk):
    patient = patient_scope(request, "billing")
    row = get_object_or_404(m.Payment.objects.select_related("invoice"), pk=pk, invoice__patient=patient)
    read_audit(request, patient, "receipt", pk)
    return download(f"CareConnect · Simulated payment receipt\nReceipt: {row.pk}\nInvoice: {row.invoice.number}\nAmount: ${row.amount}\nDate: {row.created_at.isoformat()}", f"receipt-{pk}.txt")


@api_view(["GET"])
def documents(request, pk=None, file=False):
    patient = patient_scope(request, "documents")
    read_audit(request, patient, "documents", pk or "")
    rows = patient.document_set.filter(published=True).filter(Q(encounter__published=True) | Q(encounter__isnull=True))
    if pk:
        row = get_object_or_404(rows, pk=pk)
        return download(f"{row.title}\n\n{row.content}", f"document-{pk}.txt") if file else Response(serialize(row))
    return Response(listing(rows.order_by("-pk"), ("content",)))


@api_view(["GET", "POST"])
def notifications(request):
    patient = patient_scope(request, "notifications")
    if request.method == "POST":
        data = validated(request.data, id=s.IntegerField(required=False, min_value=1))
        rows = patient.notification_set.filter(pk=data["id"]) if "id" in data else patient.notification_set.all()
        rows.update(read=True)
        return Response({"detail": "Notifications marked as read."})
    read_audit(request, patient, "notifications")
    return Response(listing(patient.notification_set.order_by("-pk")))


@api_view(["GET"])
def family(request):
    return Response([{"patient": grant.patient_id, "name": str(grant.patient), "sections": grant.sections}
                     for grant in m.ProxyAccess.objects.filter(proxy=request.user, active=True).select_related("patient__user")])
