from datetime import timedelta
from urllib.parse import parse_qs, urlsplit

import pytest
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.management import call_command
from django.utils import timezone
from rest_framework.test import APIClient
from portal.models import PasswordReset, AuditEvent, ProxyAccess

pytestmark = pytest.mark.django_db
OLD = 'CareConnect-Demo-2026!'
NEW = 'CareConnect-Test-2026!'

@pytest.fixture(autouse=True)
def setup_demo(settings):
    settings.DEBUG = settings.DEMO_MAILBOX = True
    cache.clear()
    call_command('seed_demo', verbosity=0)


def post(client, path, **data):
    return client.post('/api/'+path+'/', data, format='json')


def reset_token(client):
    response = post(client, 'password/request-reset', email='patient@careconnect.example')
    assert response.status_code == 200
    messages = client.get('/api/demo-mailbox/').json()['messages']
    return parse_qs(urlsplit(messages[0]['link']).query)['token'][0]


def test_recovery_end_to_end_single_use_and_session_revocation():
    signed_in = APIClient()
    assert post(signed_in, 'login', username='patient', password=OLD).status_code == 200
    client = APIClient()
    token = reset_token(client)
    record = PasswordReset.objects.get()
    assert record.token_hash != token and len(record.token_hash) == 64
    assert post(client, 'password/reset', token=token, password=NEW, confirm_password=NEW).status_code == 200
    assert post(client, 'password/reset', token=token, password=OLD, confirm_password=OLD).status_code == 400
    assert signed_in.get('/api/dashboard/').status_code == 403
    assert post(client, 'login', username='patient', password=OLD).status_code == 400
    assert post(client, 'login', username='patient', password=NEW).status_code == 200
    assert AuditEvent.objects.filter(action='Password reset completed').count() == 1


def test_unknown_email_generic_response_and_browser_mailbox_isolation():
    one, two = APIClient(), APIClient()
    unknown = post(one, 'password/request-reset', email='missing@example.com')
    known = post(one, 'password/request-reset', email='patient@careconnect.example')
    assert known.json() == unknown.json() and known.status_code == unknown.status_code == 200
    assert len(one.get('/api/demo-mailbox/').json()['messages']) == 1
    assert two.get('/api/demo-mailbox/').json()['messages'] == []


def test_reset_expiry_invalid_token_and_reissued_link():
    client = APIClient()
    token = reset_token(client)
    PasswordReset.objects.update(expires_at=timezone.now()-timedelta(seconds=1))
    assert post(client, 'password/reset', token=token, password=NEW, confirm_password=NEW).status_code == 400
    first, second = reset_token(client), reset_token(client)
    for invalid in (first, 'not-a-token'):
        assert post(client, 'password/reset', token=invalid, password=NEW, confirm_password=NEW).status_code == 400
    assert post(client, 'password/reset', token=second, password=NEW, confirm_password=NEW).status_code == 200


def test_confirmation_and_strength_are_enforced_without_consuming_link():
    client = APIClient()
    token = reset_token(client)
    for values in ({'password': NEW, 'confirm_password': OLD}, {'password':'12345678','confirm_password':'12345678'}, {'password':NEW}):
        assert post(client, 'password/reset', token=token, **values).status_code == 400
    assert PasswordReset.objects.get().used_at is None
    assert post(client, 'password/reset', token=token, password=NEW, confirm_password=NEW).status_code == 200


def test_password_change_confirms_and_invalidates_older_reset_link():
    client = APIClient()
    token = reset_token(client)
    assert post(client, 'login', username='patient', password=OLD).status_code == 200
    for values in ({'password':NEW}, {'password':NEW,'confirm_password':OLD}):
        assert post(client, 'password', current=OLD, **values).status_code == 400
    assert post(client, 'password', current=OLD, password=NEW, confirm_password=NEW).status_code == 200
    assert client.get('/api/dashboard/').status_code == 200
    assert post(client, 'password/reset', token=token, password=OLD, confirm_password=OLD).status_code == 400


def test_recovery_csrf_rate_limit_and_production_disabled(settings):
    client = APIClient(enforce_csrf_checks=True)
    assert post(client, 'password/request-reset', email='patient@careconnect.example').status_code == 403
    client.get('/api/session/')
    client.credentials(HTTP_X_CSRFTOKEN=client.cookies['csrftoken_v2'].value)
    for _ in range(8):
        assert post(client, 'password/request-reset', email='missing@example.com').status_code == 200
    assert post(client, 'password/request-reset', email='missing@example.com').status_code == 429
    cache.clear()
    settings.DEMO_MAILBOX = False
    assert client.get('/api/demo-mailbox/').status_code == 404
    assert post(client, 'password/request-reset', email='patient@careconnect.example').status_code == 503


def test_friendly_unavailable_errors_and_logout_removes_authorization():
    client = APIClient()
    post(client, 'login', username='patient', password=OLD)
    unavailable = client.get('/api/results/99999/')
    assert unavailable.status_code == 404
    assert 'LabResult' not in unavailable.json()['detail']
    assert 'Return to the list' in unavailable.json()['detail']
    ProxyAccess.objects.update(active=False)
    denied = client.get('/api/results/?patient=2')
    assert denied.status_code == 403
    assert 'family profile' in denied.json()['detail'] and 'ProxyAccess' not in denied.json()['detail']
    post(client, 'logout')
    assert client.get('/api/session/').json()['user'] is None
    assert client.get('/api/dashboard/').status_code == 403


def test_registration_confirms_password_and_email_is_unique():
    client = APIClient()
    details = dict(username='newpatient',first_name='River',last_name='Demo',email='river@example.com',password=NEW)
    assert post(client, 'register', **details).status_code == 400
    assert post(client, 'register', **details, confirm_password=OLD).status_code == 400
    assert post(client, 'register', **details, confirm_password=NEW).status_code == 201
    assert User.objects.get(username='newpatient').patient
    duplicate = dict(details,username='another')
    assert post(APIClient(), 'register', **duplicate,confirm_password=NEW).status_code == 400
    assert client.patch('/api/profile/',{'email':'patient@careconnect.example'}, format='json').status_code == 400
