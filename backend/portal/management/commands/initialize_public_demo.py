"""Seed a new demonstration database once; preserve accounts and edits on restarts."""
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Initialize a new explicitly enabled public demo without resetting existing data."

    def handle(self, **options):
        if settings.PUBLIC_DEMO and not User.objects.filter(username="patient").exists():
            call_command("seed_demo")
