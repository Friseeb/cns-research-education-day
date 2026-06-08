"""
Create Django superuser accounts for the organizing team.

Usage:
    python manage.py seed_organizers
"""
import secrets
import string
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

ORGANIZERS = [
    ("Sebastian Fridman", "sfridman@uwo.ca"),
    ("Kristie Lau",       "kristie.lau@lhsc.on.ca"),
    ("Elizabeth Finger",  "elizabeth.finger@lhsc.on.ca"),
]


def _random_password(length=16):
    alphabet = string.ascii_letters + string.digits + "!@#%^&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))


class Command(BaseCommand):
    help = "Create superuser accounts for the organizing team"

    def handle(self, *args, **options):
        for name, email in ORGANIZERS:
            username = email.split("@")[0].lower().replace(".", "_")
            if User.objects.filter(username=username).exists():
                self.stdout.write(f"  Already exists: {username} ({email})")
                continue
            password = _random_password()
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name=name.split()[0],
                last_name=" ".join(name.split()[1:]),
            )
            self.stdout.write(
                self.style.SUCCESS(f"Created: {username}  password: {password}  ({email})")
            )
        self.stdout.write("Done. Share passwords securely (one-time — they can change in admin).")
