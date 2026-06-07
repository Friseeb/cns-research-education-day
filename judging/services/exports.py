import csv
from io import BytesIO

from django.http import HttpResponse
from openpyxl import Workbook

from judging.models import JudgeAssignment
from judging.services.scoring import judge_adjusted_scores, rankings_for_event


def export_raw_scores(event):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{event.id}_raw_scores.csv"'
    writer = csv.writer(response)
    writer.writerow(["judge", "submission", "abstract_number", "raw_mean", "status"])
    assignments = JudgeAssignment.objects.filter(event=event).select_related(
        "judge", "submission", "score_submission"
    )
    for assignment in assignments:
        writer.writerow(
            [
                assignment.judge.name,
                assignment.submission.title,
                assignment.submission.abstract_number,
                getattr(getattr(assignment, "score_submission", None), "raw_mean", ""),
                assignment.status,
            ]
        )
    return response


def export_adjusted_rankings(event):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{event.id}_adjusted_rankings.csv"'
    writer = csv.writer(response)
    writer.writerow(
        [
            "rank",
            "abstract_number",
            "title",
            "presenting_author",
            "training_level",
            "category",
            "format",
            "final_adjusted_score",
            "final_raw_score",
            "judges_completed",
            "score_sd",
        ]
    )
    for row in rankings_for_event(event):
        writer.writerow(
            [
                row["rank"],
                row["submission"].abstract_number,
                row["submission"].title,
                row["submission"].presenting_author,
                row["submission"].get_training_level_display(),
                row["submission"].category.name,
                row["submission"].presentation_format.name,
                round(row["final_adjusted_score"], 4),
                round(row["final_raw_score"], 4),
                row["judges_completed"],
                round(row["score_sd"], 4),
            ]
        )
    return response


def export_adjusted_rankings_xlsx(event):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Adjusted Rankings"
    sheet.append(
        [
            "rank",
            "abstract_number",
            "title",
            "presenting_author",
            "training_level",
            "category",
            "format",
            "final_adjusted_score",
            "final_raw_score",
            "judges_completed",
            "score_sd",
        ]
    )
    for row in rankings_for_event(event):
        sheet.append(
            [
                row["rank"],
                row["submission"].abstract_number,
                row["submission"].title,
                row["submission"].presenting_author,
                row["submission"].get_training_level_display(),
                row["submission"].category.name,
                row["submission"].presentation_format.name,
                float(round(row["final_adjusted_score"], 4)),
                float(round(row["final_raw_score"], 4)),
                row["judges_completed"],
                float(round(row["score_sd"], 4)),
            ]
        )

    data = BytesIO()
    workbook.save(data)
    data.seek(0)
    response = HttpResponse(
        data.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{event.id}_adjusted_rankings.xlsx"'
    return response


def export_judge_completion(event):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{event.id}_judge_completion.csv"'
    writer = csv.writer(response)
    writer.writerow(["judge", "assigned", "completed", "status"])
    for judge in event.judges.all():
        assigned = judge.assignments.count()
        completed = judge.assignments.filter(status=JudgeAssignment.STATUS_SUBMITTED).count()
        status = "complete" if assigned and assigned == completed else "in_progress"
        writer.writerow([judge.name, assigned, completed, status])
    return response


def export_submission_assignments(event):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{event.id}_submission_assignments.csv"'
    writer = csv.writer(response)
    writer.writerow(["abstract_number", "title", "judge", "assignment_status"])
    assignments = JudgeAssignment.objects.filter(event=event).select_related("submission", "judge")
    for assignment in assignments:
        writer.writerow(
            [
                assignment.submission.abstract_number,
                assignment.submission.title,
                assignment.judge.name,
                assignment.status,
            ]
        )
    return response
