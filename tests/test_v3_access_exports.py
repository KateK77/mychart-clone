from datetime import timedelta
from io import BytesIO
from uuid import uuid4

import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.utils import timezone
from pypdf import PdfReader
from rest_framework.test import APIClient
from portal import models as m
from portal.exports import pdf_response

pytestmark = pytest.mark.django_db
PASSWORD = 'CareConnect-Demo-2026!'


@pytest.fixture(autouse=True)
def seed(settings):
    settings.DEBUG = True
    call_command('seed_demo', verbosity=0)


def client(username):
    c = APIClient()
    c.force_login(User.objects.get(username=username))
    return c


def post(c, route, **data):
    return c.post('/api/'+route+'/', data, format='json')


def invite(c, direction='Invite', email='caregiver@careconnect.example', **extra):
    return post(c, 'family-requests', email=email, direction=direction, relationship='Family caregiver', sections=['results'], **extra)


def test_staff_registration_requires_admin_approval_and_cannot_self_elevate():
    c = APIClient()
    data = dict(username='newdoctor', first_name='River', last_name='Stone', email='river@example.test',
                password=PASSWORD, confirm_password=PASSWORD, account_type='careteam', organization='Demo clinic')
    assert post(c, 'register', **data, requested_role='Administrator').status_code == 400
    result = post(c, 'register', **data, requested_role='Physician')
    assert result.status_code == 201
    assert result.json()['user']['application']['status'] == 'Pending'
    assert result.json()['user']['roles'] == []
    assert c.get('/api/staff/patients/').status_code == 403
    application = m.StaffApplication.objects.get(user__username='newdoctor')
    for actor in [c, client('patient'), client('physician')]:
        assert post(actor, f'access-reviews/staff/{application.pk}', action='approve', decision='Reviewed').status_code == 403
    approved = post(client('admin'), f'access-reviews/staff/{application.pk}', action='approve', decision='Demo role verified.')
    assert approved.status_code == 200
    assert c.get('/api/staff/patients/').status_code == 200
    assert c.get('/api/session/').json()['user']['roles'] == ['Physician']
    assert post(client('admin'), f'access-reviews/staff/{application.pk}', action='approve', decision='Again').status_code == 404


def test_invitation_consent_scope_revoke_and_cross_account_protection():
    owner, receiver = client('patient'), client('caregiver')
    created = invite(owner)
    assert created.status_code == 201
    pk = created.json()['id']
    own = User.objects.get(username='patient').patient
    assert receiver.get(f'/api/results/?patient={own.pk}').status_code == 403
    assert post(owner, f'family-requests/{pk}', action='accept').status_code == 403
    assert post(client('dependent'), f'family-requests/{pk}', action='accept').status_code == 404
    assert post(receiver, f'family-requests/{pk}', action='accept').status_code == 200
    assert receiver.get(f'/api/results/?patient={own.pk}').status_code == 200
    assert receiver.get(f'/api/billing/?patient={own.pk}').status_code == 403
    grant = m.ProxyAccess.objects.get(patient=own, proxy__username='caregiver')
    assert post(client('dependent'), f'family-grants/{grant.pk}/revoke').status_code == 404
    assert post(owner, f'family-grants/{grant.pk}/revoke').status_code == 200
    assert receiver.get(f'/api/results/?patient={own.pk}').status_code == 403
    assert post(receiver, f'family-requests/{pk}', action='accept').status_code == 400


def test_request_direction_decline_cancel_expiry_and_guardian_review():
    caregiver, owner = client('caregiver'), client('patient')
    row = invite(caregiver, 'Request', 'patient@careconnect.example').json()
    assert post(owner, f"family-requests/{row['id']}", action='decline').status_code == 200
    assert not m.ProxyAccess.objects.filter(proxy__username='caregiver', active=True).exists()
    row = invite(caregiver, 'Request', 'patient@careconnect.example').json()
    assert post(caregiver, f"family-requests/{row['id']}", action='cancel').status_code == 200
    row = invite(caregiver, 'Request', 'patient@careconnect.example').json()
    m.FamilyRequest.objects.filter(pk=row['id']).update(expires_at=timezone.now()-timedelta(seconds=1))
    assert post(owner, f"family-requests/{row['id']}", action='accept').status_code == 400
    row = invite(caregiver, 'Request', 'dependent@careconnect.example').json()
    assert row['status'] == 'Awaiting review'
    assert post(client('dependent'), f"family-requests/{row['id']}", action='accept').status_code == 400
    assert post(client('admin'), f"access-reviews/guardian/{row['id']}", action='approve', decision='Synthetic guardian relationship verified.').status_code == 200
    assert m.ProxyAccess.objects.filter(patient__user__username='dependent', proxy__username='caregiver', active=True).exists()


def test_new_account_receives_invitation_but_email_edits_cannot_claim_it():
    c = client('patient')
    row = invite(c, email='future@example.test').json()
    outsider = client('caregiver')
    assert outsider.patch('/api/profile/', {'email':'future@example.test'}, format='json').status_code == 200
    assert not outsider.get('/api/family-requests/').json()['requests']
    outsider.patch('/api/profile/', {'email':'caregiver@careconnect.example'}, format='json')
    new = APIClient()
    result = post(new, 'register', username='future', first_name='Future', last_name='Demo', email='future@example.test',
                  password=PASSWORD, confirm_password=PASSWORD, account_type='caregiver')
    assert result.status_code == 201
    assert new.get('/api/family-requests/').json()['requests'][0]['id'] == row['id']
    assert post(new, f"family-requests/{row['id']}", action='accept').status_code == 200


def test_restore_preserves_messages_and_only_changes_current_users_folder():
    c = client('patient')
    thread = m.Thread.objects.first()
    count = thread.messages.count()
    assert post(c, f'messages/{thread.pk}', action='archive').status_code == 200
    assert c.get(f'/api/messages/{thread.pk}/').json()['archived'] is True
    assert post(c, f'messages/{thread.pk}', action='restore').json()['detail'] == 'Conversation restored to inbox.'
    assert c.get(f'/api/messages/{thread.pk}/').json()['archived'] is False
    assert thread.messages.count() == count


def test_pdf_types_content_and_preview_match_with_object_permissions():
    c = client('patient')
    patient = User.objects.get(username='patient').patient
    lab = patient.labresult_set.first()
    document = patient.document_set.first()
    invoice = patient.invoice_set.first()
    payment = post(c, f'billing/{invoice.pk}', amount='20.25', key=str(uuid4())).json()
    for kind, pk, expected in [('lab', lab.pk, lab.name), ('document', document.pk, document.title),
                               ('invoice', invoice.pk, '$44.25'), ('receipt', payment['id'], '$20.25')]:
        endpoint = f'/api/exports/{kind}/{pk}/'
        preview = c.get(endpoint)
        assert preview.status_code == 200
        response = c.get(endpoint+'download/')
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/pdf'
        assert '.pdf' in response['Content-Disposition']
        pdf = PdfReader(BytesIO(response.content))
        text = '\n'.join(page.extract_text() for page in pdf.pages)
        assert expected in text and 'Jordan Vale' in text and 'NOT FOR CLINICAL USE' in text
        assert preview.json()['identifier'] in text
        assert client('caregiver').get(endpoint+'download/').status_code == 404
        assert client('physician').get(endpoint+'download/').status_code == 403
    lab.published = False
    lab.save()
    assert c.get(f'/api/exports/lab/{lab.pk}/download/').status_code == 404
    assert c.get(f'/api/results/{lab.pk}/download/').status_code == 404
    document.encounter.published = False
    document.encounter.save()
    assert c.get(f'/api/exports/document/{document.pk}/download/').status_code == 404
    dependent = User.objects.get(username='dependent').patient
    shared_lab = dependent.labresult_set.first()
    assert c.get(f'/api/exports/lab/{shared_lab.pk}/download/?patient={dependent.pk}').status_code == 200
    m.ProxyAccess.objects.filter(patient=dependent).update(active=False)
    assert c.get(f'/api/exports/lab/{shared_lab.pk}/download/?patient={dependent.pk}').status_code == 403


def test_long_pdf_paginates_without_losing_content():
    data = dict(title='Long synthetic report', subtitle='Clinical letter', identifier='LONG-1', date='Nov 15, 2026',
        patient='Jordan Vale', birth_date='Apr 14, 1989', facts=[['Provider','Dr. Maya Rowan']], filename='long-report.pdf',
        sections=[{'title':'Notes','body':'\n'.join(f'Line {i}: Synthetic follow-up information for the next visit.' for i in range(200))}])
    pdf = PdfReader(BytesIO(pdf_response(data).content))
    assert len(pdf.pages) > 2
    all_text = '\n'.join(page.extract_text() for page in pdf.pages)
    assert 'Line 199:' in all_text
    for i, page in enumerate(pdf.pages, 1):
        assert f'Page {i}' in page.extract_text()
