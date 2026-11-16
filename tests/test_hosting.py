import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.http import Http404
from django.test import RequestFactory

from portal.web import frontend


@pytest.mark.django_db
def test_hosted_demo_seeding_is_opt_in_and_preserves_existing_accounts(settings):
    settings.DEBUG = False
    settings.PUBLIC_DEMO = False
    with pytest.raises(CommandError):
        call_command("seed_demo")
    call_command("initialize_public_demo")
    assert not User.objects.exists()
    settings.PUBLIC_DEMO = True
    call_command("initialize_public_demo")
    patient = User.objects.get(username="patient")
    assert patient.check_password("CareConnect-Demo-2026!")
    patient.set_password("Changed-For-Persistence-2026!")
    patient.save()
    visitor = User.objects.create_user("new-visitor", password="Visitor-2026!")
    call_command("initialize_public_demo")
    patient.refresh_from_db()
    assert patient.check_password("Changed-For-Persistence-2026!")
    assert User.objects.filter(pk=visitor.pk).exists()


@pytest.mark.django_db
def test_frontend_deep_link_serves_build_without_caching(settings, tmp_path):
    settings.BASE_DIR = tmp_path / "backend"
    dist = tmp_path / "frontend" / "dist"
    dist.mkdir(parents=True)
    (dist / "index.html").write_text("<html>CareConnect</html>", encoding="utf-8")
    response = frontend(RequestFactory().get("/register"))
    assert response.status_code == 200
    assert "no-store" in response["Cache-Control"]
    assert b"CareConnect" in b"".join(response.streaming_content)
    response.close()
    (dist / "index.html").unlink()
    with pytest.raises(Http404):
        frontend(RequestFactory().get("/register"))
