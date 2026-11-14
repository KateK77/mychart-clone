from django.conf import settings
from django.db import models
from django.db.models import Q

User = settings.AUTH_USER_MODEL
ROLES = ("Physician", "Nurse", "Front Desk", "Billing Staff", "Administrator")
APPOINTMENT_TYPES = ("Primary Care", "Follow-up", "Annual Physical", "Specialist Consultation", "Telehealth", "Laboratory Visit")
APPOINTMENT_STATES = ("Scheduled", "Confirmed", "Checked In", "Completed", "Cancelled", "No Show")
LAB_STATES = ("Pending", "Preliminary", "Final", "Corrected")
CATEGORIES = ("Medical Question", "Appointment Question", "Medication Question", "Billing Question", "General Request")
REFILL_STATES = ("Requested", "Under Review", "Approved", "Denied", "Completed")
DOCUMENT_TYPES = ("After Visit Summary", "Laboratory Report", "Clinical Letter", "Visit Instructions", "Medication List", "Billing Statement", "Care Plan")
HEALTH_TYPES = ("Conditions", "Allergies", "Immunizations", "Medical history", "Surgical history", "Family history", "Social history", "Care team", "Vital signs", "Preventive care")
EVENT_TYPES = ("Test result", "Message", "Appointment", "Cancellation", "Refill", "Billing statement", "Payment")

def choices(values):
    return [(value, value) for value in values]


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="patient")
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=240, blank=True)
    muted_notifications = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Provider(models.Model):
    name = models.CharField(max_length=120)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Slot(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    starts_at = models.DateTimeField()
    kind = models.CharField(max_length=40, choices=choices(APPOINTMENT_TYPES))
    instructions = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["provider", "starts_at"], name="provider_slot_unique")]

    def __str__(self):
        return f"{self.provider} · {self.starts_at}"


class PatientRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class Appointment(PatientRecord):
    slot = models.ForeignKey(Slot, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=choices(APPOINTMENT_STATES), default="Scheduled")
    cancellation_reason = models.TextField(blank=True)
    reschedule_requested = models.BooleanField(default=False)
    reschedule_reason = models.TextField(blank=True)
    questionnaire = models.TextField(blank=True)
    predecessor = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT)
    starts_at = models.DateTimeField(editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["slot"], condition=~Q(status="Cancelled"), name="one_appointment_per_slot"),
            models.UniqueConstraint(fields=["patient", "starts_at"], condition=~Q(status="Cancelled"), name="one_appointment_per_patient_time"),
        ]

    def save(self, *args, **kwargs):
        self.starts_at = self.slot.starts_at
        super().save(*args, **kwargs)


class LabResult(PatientRecord):
    name = models.CharField(max_length=120)
    collected_at = models.DateField()
    resulted_at = models.DateField(null=True, blank=True)
    value = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    unit = models.CharField(max_length=30, blank=True)
    reference_low = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    reference_high = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=choices(LAB_STATES))
    comments = models.TextField(blank=True)
    published = models.BooleanField(default=False)

    @property
    def flag(self):
        if self.value is None:
            return ""
        if self.reference_low is not None and self.value < self.reference_low:
            return "Low"
        if self.reference_high is not None and self.value > self.reference_high:
            return "High"
        return "In range" if self.reference_low is not None or self.reference_high is not None else ""


class Medication(PatientRecord):
    name = models.CharField(max_length=120)
    strength = models.CharField(max_length=50)
    dosage = models.CharField(max_length=80)
    route = models.CharField(max_length=50)
    frequency = models.CharField(max_length=80)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    pharmacy = models.CharField(max_length=120)
    status = models.CharField(max_length=20, choices=choices(("Active", "Discontinued")), default="Active")
    instructions = models.TextField(blank=True)


class Refill(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=choices(REFILL_STATES), default="Requested")
    note = models.TextField(blank=True)
    decision = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["medication"], condition=Q(status__in=REFILL_STATES[:3]), name="one_open_refill")]


class HealthEntry(PatientRecord):
    section = models.CharField(max_length=40, choices=choices(HEALTH_TYPES))
    title = models.CharField(max_length=140)
    details = models.TextField()
    date = models.DateField(null=True, blank=True)


class Report(PatientRecord):
    topic = models.CharField(max_length=30, choices=choices(("Health summary", "Medication")))
    details = models.TextField()
    reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Encounter(PatientRecord):
    date = models.DateField()
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    kind = models.CharField(max_length=40, choices=choices(APPOINTMENT_TYPES))
    reason = models.CharField(max_length=240)
    summary = models.TextField()
    follow_up = models.TextField(blank=True)
    published = models.BooleanField(default=False)


class Diagnosis(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.PROTECT, related_name="diagnoses")
    label = models.CharField(max_length=140)
    code = models.CharField(max_length=30, blank=True)


class ClinicalNote(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.PROTECT, related_name="notes")
    title = models.CharField(max_length=120)
    body = models.TextField()
    shared = models.BooleanField(default=False)


class Thread(PatientRecord):
    subject = models.CharField(max_length=150)
    category = models.CharField(max_length=30, choices=choices(CATEGORIES))
    team = models.CharField(max_length=30, choices=choices(("Care team", "Scheduling", "Billing")))
    archived_by = models.ManyToManyField(User, blank=True, related_name="archived_threads")


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.PROTECT, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.PROTECT)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, blank=True, related_name="read_messages")


class Invoice(PatientRecord):
    number = models.CharField(max_length=40, unique=True)
    service_date = models.DateField()
    description = models.CharField(max_length=220)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    due_date = models.DateField()
    voided = models.BooleanField(default=False)

    class Meta:
        constraints = [models.CheckConstraint(condition=Q(adjustment__gte=0, paid__gte=0, amount__gte=models.F("adjustment") + models.F("paid")), name="invoice_amounts_valid")]

    @property
    def responsibility(self):
        return self.amount - self.adjustment

    @property
    def balance(self):
        return 0 if self.voided else self.responsibility - self.paid


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)
    actor = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    request_key = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["actor", "request_key"], name="payment_idempotency"),
                       models.CheckConstraint(condition=Q(amount__gt=0), name="positive_payment")]


class Insurance(PatientRecord):
    carrier = models.CharField(max_length=100)
    plan = models.CharField(max_length=100)
    member_id = models.CharField(max_length=60)


class Document(PatientRecord):
    title = models.CharField(max_length=140)
    kind = models.CharField(max_length=45, choices=choices(DOCUMENT_TYPES))
    encounter = models.ForeignKey(Encounter, on_delete=models.PROTECT, null=True, blank=True)
    content = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(PatientRecord):
    kind = models.CharField(max_length=30, choices=choices(EVENT_TYPES))
    title = models.CharField(max_length=150)
    destination = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


PROXY_SECTIONS = ("appointments", "results", "medications", "health", "visits", "billing", "documents")


class ProxyAccess(PatientRecord):
    proxy = models.ForeignKey(User, on_delete=models.PROTECT)
    sections = models.JSONField(default=list)
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["patient", "proxy"], name="unique_proxy")]


class AuditEvent(models.Model):
    actor = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True)
    action = models.CharField(max_length=60, db_index=True)
    target = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)


class PasswordReset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=64, unique=True)
    password_fingerprint = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
