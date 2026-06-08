"""
Seed realistic mock scores for all judge assignments in the active event.
Useful for testing the rankings and awards UI.

Usage:
    python manage.py seed_mock_scores           # active event
    python manage.py seed_mock_scores --clear   # wipe existing scores first
"""
import random
from django.core.management.base import BaseCommand
from judging.models import Event, JudgeAssignment, Rubric, Score, ScoreSubmission
from judging.services.scoring import upsert_score_submission


class Command(BaseCommand):
    help = "Seed mock scores for all judge assignments"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Delete existing scores first")

    def handle(self, *args, **options):
        event = Event.objects.filter(is_active=True).order_by("-date").first()
        if not event:
            self.stderr.write("No active event found.")
            return

        if options["clear"]:
            deleted = Score.objects.filter(assignment__event=event).delete()[0]
            ScoreSubmission.objects.filter(assignment__event=event).delete()
            JudgeAssignment.objects.filter(event=event).update(
                status=JudgeAssignment.STATUS_NOT_STARTED, completed_at=None
            )
            self.stdout.write(f"Cleared {deleted} scores.")

        assignments = JudgeAssignment.objects.filter(
            event=event,
            status=JudgeAssignment.STATUS_NOT_STARTED,
        ).select_related("submission", "submission__presentation_format")

        rubric_cache = {}
        seeded = 0

        for assignment in assignments:
            fmt = assignment.submission.presentation_format
            if fmt.id not in rubric_cache:
                rubric = (
                    Rubric.objects.filter(event=event, presentation_format=fmt, is_active=True)
                    .order_by("-updated_at")
                    .first()
                )
                rubric_cache[fmt.id] = rubric
            rubric = rubric_cache[fmt.id]
            if not rubric:
                self.stdout.write(f"  No rubric for {fmt.name}, skipping {assignment}")
                continue

            items = list(rubric.items.all())
            if not items:
                continue

            # Bias scores toward 3-4 to look realistic
            for item in items:
                value = random.choices([1, 2, 3, 4, 5], weights=[3, 8, 25, 40, 24])[0]
                Score.objects.update_or_create(
                    assignment=assignment,
                    rubric_item=item,
                    defaults={"value": float(value)},
                )

            comments_pool = [
                "Well-structured presentation with clear methodology.",
                "Interesting approach; would benefit from larger sample size.",
                "Excellent delivery and strong grasp of the literature.",
                "Good work — consider expanding the discussion of limitations.",
                "Clear hypothesis and appropriate statistical methods.",
                "",  # some judges leave no comment
                "",
            ]
            upsert_score_submission(
                assignment=assignment,
                comments=random.choice(comments_pool),
                is_final=True,
            )
            seeded += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded scores for {seeded} assignments."))
