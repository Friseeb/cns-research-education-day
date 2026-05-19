from django.core.management.base import BaseCommand

from judging.models import Event, PresentationFormat, Rubric, RubricItem


POSTER_ITEMS = [
    ("Scientific question", "Is the research question clear, relevant, and important?"),
    ("Methods", "Are design and analyses appropriate?"),
    ("Results", "Are results clear and complete?"),
    ("Interpretation", "Are conclusions supported by data?"),
    ("Poster design", "Is the poster readable and well organized?"),
    ("Verbal explanation", "Did presenter explain clearly?"),
    ("Response to questions", "Did presenter answer thoughtfully?"),
    ("Overall impression", "Overall quality of research and presentation."),
]

ORAL_ITEMS = [
    ("Scientific question", "Is the research question clear, relevant, and important?"),
    ("Methods", "Are design and analyses appropriate?"),
    ("Results", "Are results clear and complete?"),
    ("Interpretation", "Are conclusions supported by data?"),
    ("Slide quality", "Are slides readable and organized?"),
    ("Delivery", "Was delivery clear and confident?"),
    ("Timing", "Was time used appropriately?"),
    ("Response to questions", "Did presenter answer thoughtfully?"),
    ("Overall impression", "Overall quality of research and presentation."),
]


class Command(BaseCommand):
    help = "Create poster and oral rubrics for the active event (idempotent)"

    def handle(self, *args, **options):
        event = Event.objects.filter(is_active=True).order_by("-date").first()
        if not event:
            self.stderr.write("No active event found.")
            return

        poster_format, _ = PresentationFormat.objects.get_or_create(name="Poster presentation")
        oral_format, _ = PresentationFormat.objects.get_or_create(name="Oral presentation")

        for fmt, name, items in [
            (poster_format, "Poster rubric", POSTER_ITEMS),
            (oral_format, "Oral rubric", ORAL_ITEMS),
        ]:
            rubric, created = Rubric.objects.get_or_create(
                event=event,
                presentation_format=fmt,
                defaults={"name": name, "is_active": True},
            )
            if not created and not rubric.is_active:
                rubric.is_active = True
                rubric.save(update_fields=["is_active", "updated_at"])

            for idx, (label, desc) in enumerate(items, 1):
                RubricItem.objects.get_or_create(
                    rubric=rubric,
                    label=label,
                    defaults={"description": desc, "sort_order": idx, "min_score": 1, "max_score": 5, "weight": 1.0},
                )

            status = "created" if created else "already existed"
            self.stdout.write(f"{rubric.name} ({fmt.name}): {status}, {rubric.items.count()} items")

        self.stdout.write(self.style.SUCCESS("Rubrics ready."))
