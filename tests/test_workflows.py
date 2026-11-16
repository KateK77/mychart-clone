from decimal import Decimal
from uuid import uuid4

import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.utils import timezone
from rest_framework.test import APIClient

from portal import models as m

pytestmark = pytest.mark.django_db


@pytest.fixture
def demo(settings):
    settings.DEBUG = True
    call_command("seed_demo", verbosity=0)
    return User.objects.get(username="patient").patient


@pytest.fixture
def client_for(demo):
    def make(name, csrf=False):
        client = APIClient(enforce_csrf_checks=csrf)
        client.force_login(User.objects.get(username=name))
        return client
    return make


def post(client, route, **body):
    return client.post(f"/api/{route}/", body, format="json")


def get(client, route):
    return client.get(f"/api/{route}")


def test_a_scheduling(client_for, demo):
    patient, staff = client_for("patient"), client_for("frontdesk")
    slot = get(patient, "slots/").json()["slots"][0]
    booked = post(patient, "appointments", slot=slot["id"])
    assert booked.status_code == 201
    pk = booked.json()["id"]
    assert post(client_for("dependent"), "appointments", slot=slot["id"]).status_code in (400, 404)
    assert pk in [row["id"] for row in get(patient, "dashboard/").json()["appointments"]]
    assert get(staff, f"staff/appointments/{pk}/").json()["patient"] == demo.id
    assert post(patient, f"appointments/{pk}", action="check-in").status_code == 400
    assert post(patient, f"appointments/{pk}", action="reschedule", note="Next Tuesday").json()["reschedule_requested"]
    replacement = get(patient, "slots/").json()["slots"][0]["id"]
    moved = post(staff, f"staff/appointments/{pk}", action="reschedule", slot=replacement).json()
    assert moved["predecessor"] == pk
    pk = moved["id"]
    assert post(patient, f"appointments/{pk}", action="questionnaire", note="Routine care").status_code == 200
    assert post(patient, f"appointments/{pk}", action="check-in").json()["status"] == "Checked In"
    assert post(staff, f"staff/appointments/{pk}", action="status", status="Completed").status_code == 200
    assert post(patient, f"appointments/{pk}", action="cancel", note="Conflict").status_code == 400
    assert m.AuditEvent.objects.filter(action="Appointment Completed", target=str(pk)).exists()


def test_b_lab_publication(client_for, demo):
    patient, staff = client_for("patient"), client_for("physician")
    provider = m.Provider.objects.first()
    today = timezone.localdate().isoformat()
    response = post(staff, "staff/results", patient=demo.id, provider=provider.id, name="Hemoglobin A1c",
                    collected_at=today, resulted_at=today, value="6.10", unit="%",
                    reference_low="4", reference_high="5.6", status="Final")
    assert response.status_code == 201, response.content
    pk = response.json()["id"]
    assert get(patient, f"results/{pk}/").status_code == 404
    assert post(client_for("billing"), f"staff/results/{pk}", published=True).status_code == 403
    assert post(staff, f"staff/results/{pk}", published=True).status_code == 200
    assert f"/results/{pk}" in [row["destination"] for row in get(patient, "notifications/").json()]
    result = get(patient, f"results/{pk}/").json()
    assert result["flag"] == "High"
    assert len(result["history"]) == 4
    assert get(patient, f"results/{pk}/download/").status_code == 200
    assert get(client_for("dependent"), f"results/{pk}/").status_code == 404


def test_c_thread(client_for):
    patient, staff = client_for("patient"), client_for("nurse")
    response = post(patient, "messages", subject="Synthetic question", category="Medical Question", team="Care team", body="Hello")
    assert response.status_code == 201
    pk = response.json()["id"]
    assert get(client_for("billing"), f"messages/{pk}/").status_code == 404
    assert get(staff, f"messages/{pk}/").json()["messages"][0]["body"] == "Hello"
    assert post(staff, f"messages/{pk}", action="reply", body="Follow-up").status_code == 201
    assert f"/messages/{pk}" in [row["destination"] for row in get(patient, "notifications/").json()]
    assert get(patient, f"messages/{pk}/").json()["messages"][-1]["body"] == "Follow-up"
    assert next(row for row in get(patient, "messages/").json() if row["id"] == pk)["unread"] == 0


def test_d_refill(client_for, demo):
    patient, staff = client_for("patient"), client_for("physician")
    med = demo.medication_set.first()
    refill = post(patient, f"medications/{med.id}", note="Synthetic request")
    assert refill.status_code == 201
    assert post(patient, f"medications/{med.id}", note="Duplicate").status_code == 400
    pk = refill.json()["id"]
    assert post(staff, f"staff/refills/{pk}", status="Completed").status_code == 400
    for status in ("Under Review", "Approved", "Completed"):
        assert post(staff, f"staff/refills/{pk}", status=status).status_code == 200
    assert get(patient, f"medications/{med.id}/").json()["refills"][0]["status"] == "Completed"


def test_e_billing(client_for, demo):
    patient, staff = client_for("patient"), client_for("billing")
    today = timezone.localdate().isoformat()
    response = post(staff, "staff/billing", patient=demo.id, number="CC-TEST", description="Synthetic visit",
                    service_date=today, due_date=today, amount="110.00", adjustment="60.00")
    assert response.status_code == 201, response.content
    pk = response.json()["id"]
    assert get(patient, f"billing/{pk}/").json()["balance"] == "50.00"
    key = str(uuid4())
    for _ in range(2):
        paid = post(patient, f"billing/{pk}", amount="20.25", key=key)
        assert paid.status_code == 201, paid.content
    assert m.Payment.objects.filter(invoice_id=pk).count() == 1
    assert Decimal(get(patient, f"billing/{pk}/").json()["balance"]) == Decimal("29.75")
    assert get(patient, f"billing/receipt/{paid.json()['id']}/").status_code == 200
    assert post(patient, f"billing/{pk}", amount="100.00", key=str(uuid4())).status_code == 400


def test_f_proxy(client_for, demo):
    patient, admin, dependent = client_for("patient"), client_for("admin"), User.objects.get(username="dependent").patient
    grant = post(admin, "staff/proxy", patient=demo.id, proxy=dependent.user_id, sections=["documents"], active=True)
    assert grant.status_code == 201
    proxy = client_for("dependent")
    doc = demo.document_set.first()
    assert get(proxy, f"documents/{doc.id}/download/").status_code == 404
    assert get(proxy, f"documents/{doc.id}/download/?patient={demo.id}").status_code == 200
    assert get(proxy, f"billing/?patient={demo.id}").status_code == 403
    assert post(patient, "staff/proxy", patient=demo.id, proxy=dependent.user_id, sections=["billing"]).status_code == 403
    assert admin.patch(f"/api/staff/proxy/{grant.json()['id']}/", {"active": False}, format="json").status_code == 200
    assert get(proxy, f"documents/{doc.id}/download/?patient={demo.id}").status_code == 403
    assert m.AuditEvent.objects.filter(action="Staff changed proxy", patient=demo).count() == 2


def test_authentication_csrf_and_validation(demo):
    client = APIClient(enforce_csrf_checks=True)
    assert get(client, "dashboard/").status_code == 403
    assert post(client, "login", username="patient", password="wrong").status_code == 403
    csrf = get(client, "session/").cookies["csrftoken_v3"].value
    client.credentials(HTTP_X_CSRFTOKEN=csrf)
    assert post(client, "login", username="patient", password="wrong").status_code == 400
    assert post(client, "login", username="patient", password="CareConnect-Demo-2026!").status_code == 200
    client.credentials(HTTP_X_CSRFTOKEN=client.cookies["csrftoken_v3"].value)
    assert get(client, "dashboard/").status_code == 200
    assert post(client, "appointments", slot=-5).status_code == 400
    assert post(client, "logout").status_code == 200
    assert m.AuditEvent.objects.filter(action="Login", patient=demo).exists()


def test_visit_privacy_and_correction_request(client_for, demo):
    patient = client_for("patient")
    visit = demo.encounter_set.first()
    shared = get(patient, f"visits/{visit.id}/").json()
    assert [note["title"] for note in shared["notes"]] == ["Visit note"]
    assert post(patient, "report", topic="Health summary", details="Review history").status_code == 201
    assert get(client_for("physician"), "staff/reports/").json()[0]["details"] == "Review history"
    assert get(client_for("frontdesk"), "staff/reports/").status_code == 403
