import openpyxl
from django.core.management.base import BaseCommand, CommandError
from judging.models import Event, Category, PresentationFormat, Submission

CATEGORY_MAP = {
    "resident": "Resident",
    "master's student": "Graduate Student",
    "masters student": "Graduate Student",
    "phd student": "Graduate Student",
    "undergraduate student": "Undergraduate Student",
    "medical student": "Medical Student",
    "clinical fellow": "Fellow",
    "fellow": "Fellow",
    "research fellow": "Fellow",
    "post-doctoral fellow": "Fellow",
    "postdoctoral fellow": "Fellow",
    "research associate": "Faculty/Staff",
    "research assistant": "Faculty/Staff",
}


class Command(BaseCommand):
    help = "Import submissions from the CNS Research Day xlsx tracker"

    def add_arguments(self, parser):
        parser.add_argument("xlsx_path", type=str, help="Path to the xlsx file")
        parser.add_argument("--event", type=str, default="CNS Research Day 2026")
        parser.add_argument("--clear", action="store_true", help="Delete existing submissions before importing")

    def handle(self, *args, **options):
        try:
            wb = openpyxl.load_workbook(options["xlsx_path"])
        except FileNotFoundError:
            raise CommandError(f"File not found: {options['xlsx_path']}")

        event, _ = Event.objects.get_or_create(
            name=options["event"],
            defaults={"is_active": True},
        )
        self.stdout.write(f"Event: {event.name}")

        oral_format, _ = PresentationFormat.objects.get_or_create(name="Oral presentation")
        poster_format, _ = PresentationFormat.objects.get_or_create(name="Poster presentation")

        if options["clear"]:
            deleted, _ = Submission.objects.filter(event=event).delete()
            self.stdout.write(f"Deleted {deleted} existing submissions.")

        ws = wb["Completed"]
        rows = list(ws.iter_rows(values_only=True))

        header = None
        created = 0
        skipped = 0

        for row in rows:
            if row[1] == "First Name" and row[2] == "Last Name":
                header = row
                continue
            if not any(row):
                continue

            first_name = str(row[1] or "").strip()
            last_name = str(row[2] or "").strip()
            email = str(row[3] or "").strip()
            role_raw = str(row[4] or "").strip()
            title = str(row[5] or "").strip()
            format_raw = str(row[9] or "").strip().lower()
            tag = str(row[10] or "").strip()
            session = str(row[11] or "").strip()
            time_str = str(row[12] or "").strip()
            location = str(row[13] or "").strip()

            if not first_name or not title or not tag:
                skipped += 1
                continue

            category_name = CATEGORY_MAP.get(role_raw.lower(), role_raw)
            category, _ = Category.objects.get_or_create(event=event, name=category_name)

            fmt = oral_format if "oral" in format_raw else poster_format

            presenting_author = f"{first_name} {last_name}".strip()

            location_full = f"{session} | {time_str} | {location}".strip(" |")

            obj, created_now = Submission.objects.update_or_create(
                event=event,
                abstract_number=tag,
                defaults={
                    "title": title,
                    "presenting_author": presenting_author,
                    "category": category,
                    "presentation_format": fmt,
                    "location": location_full,
                    "is_active": True,
                },
            )
            if created_now:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. {created} submissions created, {skipped} rows skipped."
        ))
        self.stdout.write(f"Total submissions: {Submission.objects.filter(event=event).count()}")
