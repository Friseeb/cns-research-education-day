from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Send a test judge invite email to a given address, rendered as a specific judge."

    def add_arguments(self, parser):
        parser.add_argument("--to", required=True, help="Recipient email address")
        parser.add_argument("--judge", default="Chris Watling", help="Judge name to render (default: Chris Watling)")

    def handle(self, *args, **options):
        from judging.models import Event, Judge
        from judging.services.email import send_judge_invite, _sendgrid_send
        import judging.services.email as em

        event = Event.objects.filter(is_active=True).first()
        if not event:
            raise CommandError("No active event found.")

        judge_name = options["judge"]
        judge = Judge.objects.filter(event=event, name__icontains=judge_name).first()
        if not judge:
            raise CommandError(f"Judge '{judge_name}' not found. Available: {', '.join(Judge.objects.filter(event=event).values_list('name', flat=True))}")

        to_email = options["to"]

        # Override recipient without changing the judge record
        original_send = em._sendgrid_send
        def patched_send(to, name, subject, body_html, body_text):
            original_send(to_email, name, subject, body_html, body_text)
        em._sendgrid_send = patched_send

        try:
            send_judge_invite(judge, "https://westerncnsday.org")
        finally:
            em._sendgrid_send = original_send

        self.stdout.write(self.style.SUCCESS(f"Test email sent to {to_email} (rendered as {judge.name})."))
