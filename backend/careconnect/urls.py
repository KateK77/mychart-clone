from django.http import JsonResponse
from django.urls import path
from django.db import connection

from portal import auth, messages, patient, staff, recovery


def healthcheck(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("api/healthcheck/", healthcheck),
    path("api/session/", auth.session),
    path("api/login/", auth.sign_in),
    path("api/logout/", auth.sign_out),
    path("api/register/", auth.register),
    path("api/profile/", auth.profile),
    path("api/password/", auth.password),
    path("api/password/request-reset/", recovery.request_reset),
    path("api/password/reset/", recovery.reset_password),
    path("api/demo-mailbox/", recovery.mailbox),
    path("api/dashboard/", patient.dashboard),
    path("api/slots/", patient.slots),
    path("api/report/", patient.report),
    path("api/health/", patient.health),
    path("api/family/", patient.family),
    path("api/notifications/", patient.notifications),
    path("api/billing/receipt/<int:pk>/", patient.receipt),
    path("api/results/<int:pk>/download/", patient.results, {"file": True}),
    path("api/documents/<int:pk>/download/", patient.documents, {"file": True}),
    path("api/staff/patients/", staff.patients),
    path("api/staff/<slug:resource>/", staff.records),
    path("api/staff/<slug:resource>/<int:pk>/", staff.records),
]
for route, view in (
    ("appointments", patient.appointments), ("results", patient.results), ("messages", messages.threads),
    ("medications", patient.medications), ("visits", patient.visits), ("billing", patient.billing),
    ("documents", patient.documents),
):
    urlpatterns.extend([path(f"api/{route}/", view), path(f"api/{route}/<int:pk>/", view)])
