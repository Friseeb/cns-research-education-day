from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from judging.models import (
    Category,
    Event,
    Judge,
    JudgeAssignment,
    PresentationFormat,
    Rubric,
    RubricItem,
    Score,
)
from judging.services.scoring import upsert_score_submission


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
    help = "Create a demo CNS Research Day event with sample data"

    def handle(self, *args, **options):
        event, _ = Event.objects.get_or_create(
            name="CNS Research Day 2026",
            defaults={"date": date(2026, 5, 14), "is_active": True},
        )

        categories = {}
        for idx, name in enumerate(["Medical student", "Graduate student", "Resident", "Fellow"]):
            categories[name], _ = Category.objects.get_or_create(
                event=event,
                name=name,
                defaults={"sort_order": idx},
            )

        poster_format, _ = PresentationFormat.objects.get_or_create(name="Poster presentation")
        oral_format, _ = PresentationFormat.objects.get_or_create(name="Oral presentation")

        poster_rubric, _ = Rubric.objects.get_or_create(
            event=event,
            name="Poster rubric",
            presentation_format=poster_format,
            defaults={"is_active": True},
        )
        oral_rubric, _ = Rubric.objects.get_or_create(
            event=event,
            name="Oral rubric",
            presentation_format=oral_format,
            defaults={"is_active": True},
        )

        for idx, (label, desc) in enumerate(POSTER_ITEMS, 1):
            RubricItem.objects.get_or_create(
                rubric=poster_rubric,
                label=label,
                defaults={"description": desc, "sort_order": idx, "min_score": 1, "max_score": 5, "weight": 1.0},
            )

        for idx, (label, desc) in enumerate(ORAL_ITEMS, 1):
            RubricItem.objects.get_or_create(
                rubric=oral_rubric,
                label=label,
                defaults={"description": desc, "sort_order": idx, "min_score": 1, "max_score": 5, "weight": 1.0},
            )

        submissions = []
        from judging.models import Submission

        for i in range(1, 7):
            sub, _ = Submission.objects.get_or_create(
                event=event,
                abstract_number=f"A{i:03d}",
                defaults={
                    "title": f"Neuro study {i}",
                    "presenting_author": f"Presenter {i}",
                    "co_authors": "Coauthor A; Coauthor B",
                    "category": categories["Resident" if i % 2 else "Graduate student"],
                    "presentation_format": poster_format if i % 2 else oral_format,
                    "abstract_text": f"This is sample abstract text for submission {i}.",
                    "presentation_time": timezone.now() + timedelta(hours=i),
                    "location": f"Board {i}",
                },
            )
            submissions.append(sub)

        judges = []
        for i in range(1, 5):
            judge, _ = Judge.objects.get_or_create(
                event=event,
                email=f"judge{i}@example.com",
                defaults={"name": f"Judge {i}", "affiliation": "CNS Faculty"},
            )
            judges.append(judge)

        for idx, submission in enumerate(submissions):
            for judge in judges:
                assignment, _ = JudgeAssignment.objects.get_or_create(
                    event=event,
                    judge=judge,
                    submission=submission,
                )
                if (idx + judge.id) % 2 == 0:
                    rubric = poster_rubric if submission.presentation_format == poster_format else oral_rubric
                    for item in rubric.items.all():
                        Score.objects.update_or_create(
                            assignment=assignment,
                            rubric_item=item,
                            defaults={"value": float(((idx + item.sort_order + judge.id) % 5) + 1)},
                        )
                    upsert_score_submission(
                        assignment=assignment,
                        comments="Demo completed score",
                        is_final=True,
                    )

        self.stdout.write(self.style.SUCCESS("Demo CNS event created or updated."))
