import os
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from portal import models as m


class Command(BaseCommand):
    help = "Create repeatable synthetic demo records in the local database."

    @transaction.atomic
    def handle(self, **options):
        if not settings.DEBUG:
            raise CommandError("Synthetic demo accounts can only be seeded in local mode.")
        now = timezone.now()
        today = now.date()
        password = os.getenv("CC_DEMO_PASSWORD", "CareConnect-Demo-2026!")
        people = (
            ("caregiver", "Taylor", "Vale", None), ("patient", "Jordan", "Vale", None), ("dependent", "Avery", "Vale", None),
            ("physician", "Maya", "Rowan", "Physician"), ("nurse", "Theo", "Lark", "Nurse"),
            ("frontdesk", "Riley", "Quill", "Front Desk"), ("billing", "Sam", "Voss", "Billing Staff"),
            ("admin", "Morgan", "Wren", "Administrator"),
        )
        accounts = {}
        for username, first, last, role in people:
            user, created = User.objects.get_or_create(username=username, defaults={
                "first_name": first, "last_name": last, "email": f"{username}@careconnect.example",
            })
            if created:
                user.set_password(password)
                user.save(update_fields=["password"])
                if role:
                    user.groups.add(Group.objects.get_or_create(name=role)[0])
            accounts[username] = user
        patient, _ = m.Patient.objects.get_or_create(user=accounts["patient"], defaults={"birth_date": "1989-04-14", "phone": "(312) 555-0148"})
        m.Patient.objects.get_or_create(user=accounts["caregiver"], defaults={"account_kind": "Caregiver", "birth_date": "1985-06-10"})
        dependent, _ = m.Patient.objects.get_or_create(user=accounts["dependent"], defaults={"birth_date": "2016-09-22"})
        m.ProxyAccess.objects.get_or_create(patient=dependent, proxy=accounts["patient"], defaults={"sections": ["appointments", "results", "visits"]})
        providers = []
        for name, department in (("Dr. Maya Rowan", "Primary Care"), ("Dr. Elian Moss", "Cardiology"), ("Jamie Arden, NP", "Laboratory Services")):
            dept, _ = m.Department.objects.get_or_create(name=department)
            providers.append(m.Provider.objects.get_or_create(name=name, department=dept)[0])
        provider = providers[0]
        at = now.replace(hour=15, minute=30, second=0, microsecond=0)
        for index, kind in enumerate(m.APPOINTMENT_TYPES):
            p = providers[index % len(providers)]
            for day in (3, 7, 12):
                m.Slot.objects.get_or_create(provider=p, starts_at=at + timedelta(days=day + index), defaults={
                    "kind": kind, "instructions": "Please arrive 15 minutes before your scheduled visit.",
                })
        if not patient.appointment_set.exists():
            for offset, status, kind in [(2, "Confirmed", "Annual Physical"), (-18, "Completed", "Primary Care")]:
                slot, _ = m.Slot.objects.get_or_create(provider=provider, starts_at=at + timedelta(days=offset),
                    defaults={"kind": kind, "instructions": "Bring your current medication list and arrive 15 minutes early."})
                m.Appointment.objects.create(patient=patient, slot=slot, status=status)
        for label, unit, low, high, values in [
            ("Hemoglobin A1c", "%", "4.0", "5.6", ["5.6", "5.7", "5.8"]),
            ("Total cholesterol", "mg/dL", "120", "199", ["171", "179", "182"]),
        ]:
            if not patient.labresult_set.filter(name=label).exists():
                for index, value in enumerate(values):
                    collected = today - timedelta(days=12 + (2 - index) * 90)
                    m.LabResult.objects.create(patient=patient, provider=provider, name=label, unit=unit, value=value,
                        reference_low=low, reference_high=high, collected_at=collected,
                        resulted_at=collected + timedelta(days=1), status="Final", published=True,
                        comments="Reviewed by your care team. Discuss any questions at your next visit.")
        for name, strength in [("Cetirizine", "10 mg"), ("Vitamin D3", "1000 IU")]:
            m.Medication.objects.get_or_create(patient=patient, name=name, defaults={
                "strength": strength, "dosage": "1 tablet", "route": "Oral", "frequency": "Daily",
                "start_date": today - timedelta(days=90), "provider": provider, "pharmacy": "Willow Demo Pharmacy",
                "instructions": "Synthetic demonstration record.",
            })
        for section, title, details in [
            ("Conditions", "Seasonal allergies", "Reviewed at the most recent primary care visit."),
            ("Allergies", "No known drug allergies", "Reviewed with patient."),
            ("Immunizations", "Influenza", "Seasonal vaccine documented."),
            ("Medical history", "Seasonal rhinitis", "History reviewed."),
            ("Surgical history", "History reviewed", "No procedures documented."),
            ("Family history", "History reviewed", "Family history discussed at visit."),
            ("Social history", "Activity", "Walks several times per week."),
            ("Care team", "Dr. Maya Rowan", "Primary Care"),
            ("Vital signs", "Blood pressure", "118/76 mmHg"),
            ("Preventive care", "Annual physical", "Visit scheduled."),
        ]:
            m.HealthEntry.objects.get_or_create(patient=patient, section=section, title=title, defaults={"details": details, "date": today})
        if not patient.encounter_set.exists():
            visit = m.Encounter.objects.create(patient=patient, date=today - timedelta(days=18),
                provider=provider, kind="Primary Care", reason="Routine primary care follow-up", published=True,
                summary="Reviewed preventive care, current medications and recent lab orders.", follow_up="Return for your scheduled annual physical.")
            m.Diagnosis.objects.create(encounter=visit, label="Seasonal allergic rhinitis", code="J30.2")
            m.ClinicalNote.objects.create(encounter=visit, title="Visit note", body="Patient questions were reviewed.", shared=True)
            m.ClinicalNote.objects.create(encounter=visit, title="Internal note", body="Synthetic internal note.", shared=False)
            m.Document.objects.create(patient=patient, encounter=visit, title="Primary care visit summary",
                kind="After Visit Summary", published=True, content=visit.summary + "\n\n" + visit.follow_up)
        if not patient.thread_set.exists():
            thread = m.Thread.objects.create(patient=patient, subject="Your upcoming physical", category="Appointment Question", team="Scheduling")
            m.Message.objects.create(thread=thread, sender=accounts["frontdesk"], body="Hello Jordan, please bring your current medications to your upcoming physical.")
            m.Notification.objects.create(patient=patient, kind="Message", title="Message from your care team", destination=f"/messages/{thread.pk}")
        m.Invoice.objects.get_or_create(number="CC-1001", defaults={"patient": patient, "service_date": today - timedelta(days=18),
            "description": "Primary care office visit", "amount": Decimal("180"), "adjustment": Decimal("115.50"),
            "due_date": today + timedelta(days=15)})
        m.Insurance.objects.get_or_create(patient=patient, carrier="Willow Demo Health", defaults={"plan": "Synthetic PPO", "member_id": "DEMO-0001"})
        m.LabResult.objects.get_or_create(patient=dependent, name="Hemoglobin", defaults={
            "provider": provider, "collected_at": today, "resulted_at": today, "value": "13.1", "unit": "g/dL",
            "reference_low": "11.5", "reference_high": "15.5", "status": "Final", "published": True,
        })
        self.stdout.write(self.style.SUCCESS("Synthetic CareConnect records are ready."))
