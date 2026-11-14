from django.utils import timezone
from rest_framework import serializers as s

from . import models as m


class Input(s.Serializer):
    def validate(self, data):
        unknown = set(self.initial_data) - set(self.fields)
        if unknown:
            raise s.ValidationError({key: "Unknown field." for key in sorted(unknown)})
        return data


def validated(data, **fields):
    cls = type("RequestFields", (Input,), fields)
    serializer = cls(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


def text(required=True, length=4000):
    return s.CharField(max_length=length, required=required, allow_blank=not required)


def select(options):
    return s.ChoiceField(choices=options)


class RecordSerializer(s.ModelSerializer):
    def validate(self, attrs):
        unknown = set(self.initial_data) - {name for name, field in self.fields.items() if not field.read_only}
        if unknown:
            raise s.ValidationError({key: "Unknown or read-only field." for key in sorted(unknown)})
        def value(key, default=None):
            return attrs.get(key, getattr(self.instance, key, default))
        model = self.Meta.model
        pairs = {
            m.LabResult: ("reference_low", "reference_high", "Reference range is reversed."),
            m.Medication: ("start_date", "end_date", "End date precedes start date."),
            m.Invoice: ("service_date", "due_date", "Due date precedes service date."),
        }
        if model in pairs:
            first, last, message = pairs[model]
            if value(first) is not None and value(last) is not None and value(first) > value(last):
                raise s.ValidationError(message)
        if model is m.LabResult:
            if value("resulted_at") and value("resulted_at") < value("collected_at"):
                raise s.ValidationError("Result date precedes collection date.")
            if value("value") is not None and not value("unit"):
                raise s.ValidationError("Specify the unit for numeric values.")
        if model is m.Invoice:
            amount, adjustment, paid = value("amount"), value("adjustment", 0), value("paid", 0)
            if min(amount, adjustment) < 0 or adjustment + paid > amount:
                raise s.ValidationError("Invoice totals are inconsistent.")
        if model is m.Document and value("encounter") and value("encounter").patient_id != value("patient").pk:
            raise s.ValidationError("Select an encounter for the same patient.")
        if model is m.Slot and self.instance and m.Appointment.objects.filter(slot=self.instance).exists():
            if {"starts_at", "provider", "kind"}.intersection(attrs):
                raise s.ValidationError("Booked slots keep their original time, provider and visit type.")
        return attrs


def fields_for(model, exclude=(), readonly=()):
    meta = type("Meta", (), {"model": model, "fields": [f.name for f in model._meta.fields if f.name not in exclude],
                              "read_only_fields": readonly})
    return type(f"{model.__name__}Serializer", (RecordSerializer,), {"Meta": meta})


def serialize(obj, exclude=()):
    result = dict(fields_for(type(obj), exclude)(obj).data)
    if hasattr(obj, "provider"):
        result["provider_name"] = obj.provider.name
        result["department"] = obj.provider.department.name
    if isinstance(obj, m.Slot):
        from .services import available_slots
        result.update(available=available_slots().filter(pk=obj.pk).exists(),
                      booked=m.Appointment.objects.filter(slot=obj).exists())
    if isinstance(obj, m.Appointment):
        result.update(provider_name=obj.slot.provider.name, kind=obj.slot.kind, instructions=obj.slot.instructions,
                      department=obj.slot.provider.department.name)
    if isinstance(obj, m.LabResult):
        result["flag"] = obj.flag
    if isinstance(obj, m.Refill):
        result["medication_name"] = obj.medication.name
    if isinstance(obj, m.Invoice):
        result.update(responsibility=str(obj.responsibility), balance=str(obj.balance), status=(
            "Voided" if obj.voided else "Paid" if not obj.balance else "Overdue" if obj.due_date < timezone.localdate()
            else "Partially Paid" if obj.paid else "Unpaid"))
    return result
