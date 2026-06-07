from collections import defaultdict
from statistics import mean, median

from django.db.models import StdDev

from judging.models import JudgeAssignment, Score, ScoreSubmission


def calculate_raw_score(assignment):
    scores = Score.objects.filter(assignment=assignment).select_related("rubric_item")
    total_weight = 0.0
    weighted_sum = 0.0
    for score in scores:
        weight = score.rubric_item.weight
        weighted_sum += score.value * weight
        total_weight += weight
    if total_weight == 0:
        return 0.0
    return weighted_sum / total_weight


def upsert_score_submission(assignment, comments="", is_final=False):
    raw_mean = calculate_raw_score(assignment)
    summary, _ = ScoreSubmission.objects.get_or_create(assignment=assignment)
    score_count = assignment.scores.count()
    summary.raw_mean = raw_mean
    summary.raw_total = raw_mean * score_count
    summary.comments = comments
    summary.is_final = is_final
    if is_final:
        from django.utils import timezone

        now = timezone.now()
        summary.submitted_at = now
        summary.time_submitted = now
        if not summary.time_started:
            summary.time_started = assignment.assigned_at
        summary.time_spent_seconds = int((summary.time_submitted - summary.time_started).total_seconds())
        assignment.status = JudgeAssignment.STATUS_SUBMITTED
        assignment.completed_at = now
        assignment.save(update_fields=["status", "completed_at", "updated_at"])
    else:
        assignment.status = JudgeAssignment.STATUS_DRAFT
        assignment.save(update_fields=["status", "updated_at"])
    summary.save()
    return summary


def judge_adjusted_scores(event):
    completed = list(
        ScoreSubmission.objects.filter(
            assignment__event=event,
            is_final=True,
            assignment__status=JudgeAssignment.STATUS_SUBMITTED,
        ).select_related("assignment__judge", "assignment__submission")
    )
    by_judge = defaultdict(list)
    for row in completed:
        by_judge[row.assignment.judge_id].append(row.raw_mean)

    out = {}
    for row in completed:
        judge_values = by_judge[row.assignment.judge_id]
        judge_med = median(judge_values)
        adjusted = row.raw_mean - judge_med
        iqr = None
        if len(judge_values) >= 4:
            ordered = sorted(judge_values)
            q1 = ordered[len(ordered) // 4]
            q3 = ordered[(len(ordered) * 3) // 4]
            iqr = q3 - q1
            if iqr and iqr > 0:
                adjusted = (row.raw_mean - judge_med) / iqr
        out[row.assignment_id] = {
            "raw_mean": row.raw_mean,
            "judge_median": judge_med,
            "judge_iqr": iqr,
            "adjusted": adjusted,
        }
    return out


def rankings_for_event(event, category_id=None, format_id=None):
    assignments = JudgeAssignment.objects.filter(
        event=event,
        status=JudgeAssignment.STATUS_SUBMITTED,
        score_submission__is_final=True,
        submission__award_eligible=True,
    ).select_related("submission", "submission__category", "submission__presentation_format")

    if category_id:
        assignments = assignments.filter(submission__category_id=category_id)
    if format_id:
        assignments = assignments.filter(submission__presentation_format_id=format_id)

    adjusted_map = judge_adjusted_scores(event)
    grouped = defaultdict(list)
    for assignment in assignments.select_related("judge"):
        key = assignment.submission_id
        entry = adjusted_map.get(assignment.id)
        if not entry:
            continue
        grouped[key].append({**entry, "judge_name": assignment.judge.name})

    rows = []
    for submission_id, score_rows in grouped.items():
        first_assignment = assignments.filter(submission_id=submission_id).first()
        if not first_assignment:
            continue
        submission = first_assignment.submission
        adjusted_values = [r["adjusted"] for r in score_rows]
        raw_values = [r["raw_mean"] for r in score_rows]
        rows.append(
            {
                "submission": submission,
                "final_adjusted_score": mean(adjusted_values),
                "final_raw_score": mean(raw_values),
                "judges_completed": len(raw_values),
                "judge_scores": [
                    {"name": r["judge_name"], "raw_mean": round(r["raw_mean"], 2)}
                    for r in score_rows
                ],
                "score_sd": (
                    JudgeAssignment.objects.filter(
                        submission=submission,
                        score_submission__is_final=True,
                        status=JudgeAssignment.STATUS_SUBMITTED,
                    ).aggregate(sd=StdDev("score_submission__raw_mean"))["sd"]
                    or 0
                ),
            }
        )

    rows.sort(key=lambda r: (r["final_adjusted_score"], r["final_raw_score"]), reverse=True)

    if rows:
        min_adj = min(r["final_adjusted_score"] for r in rows)
        max_adj = max(r["final_adjusted_score"] for r in rows)
        span = max_adj - min_adj
        for row in rows:
            row["final_adjusted_score"] = (
                1 + (row["final_adjusted_score"] - min_adj) / span * 4 if span > 0 else 3.0
            )

    for idx, row in enumerate(rows, 1):
        row["rank"] = idx
    return rows


def judge_metrics(event):
    judges = event.judges.all().prefetch_related("assignments__score_submission")
    data = []
    for judge in judges:
        submitted = [a for a in judge.assignments.all() if a.status == JudgeAssignment.STATUS_SUBMITTED]
        raw_scores = [a.score_submission.raw_mean for a in submitted if hasattr(a, "score_submission")]
        med = median(raw_scores) if raw_scores else 0
        iqr = 0
        if len(raw_scores) >= 4:
            ordered = sorted(raw_scores)
            iqr = ordered[(len(ordered) * 3) // 4] - ordered[len(ordered) // 4]
        completion = 0
        if judge.assignments.count() > 0:
            completion = round(100 * len(submitted) / judge.assignments.count(), 1)
        data.append(
            {
                "judge": judge,
                "assigned": judge.assignments.count(),
                "completed": len(submitted),
                "median_raw": med,
                "iqr_raw": iqr,
                "completion_pct": completion,
            }
        )
    return data
