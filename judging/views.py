from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

import qrcode
import qrcode.image.svg

from .forms import CSVUploadForm, ScoreSubmissionForm
from .models import Event, Judge, JudgeAssignment, Rubric, RubricItem, Score, Submission
from .services.exports import (
	export_adjusted_rankings,
	export_adjusted_rankings_xlsx,
	export_judge_completion,
	export_raw_scores,
	export_submission_assignments,
)
from .services.imports import import_assignments, import_judges, import_submissions
from .services.scoring import judge_metrics, rankings_for_event, upsert_score_submission


def landing_page(request):
	return render(request, "judging/landing.html")


def _get_judge_by_token(token):
	return get_object_or_404(Judge, token=token, is_active=True)


def judge_dashboard(request, token):
	judge = _get_judge_by_token(token)
	request.session["judge_token"] = token
	assignments = (
		JudgeAssignment.objects.filter(judge=judge)
		.select_related("submission", "submission__category", "submission__presentation_format")
		.order_by("submission__abstract_number")
	)
	context = {
		"judge": judge,
		"assignments": assignments,
	}
	return render(request, "judging/judge_dashboard.html", context)


def score_submission(request, token, submission_id):
	judge = _get_judge_by_token(token)
	assignment = get_object_or_404(
		JudgeAssignment.objects.select_related(
			"submission",
			"submission__category",
			"submission__presentation_format",
			"submission__event",
		),
		judge=judge,
		submission_id=submission_id,
	)
	submission = assignment.submission

	rubric = (
		Rubric.objects.filter(
			event=submission.event,
			presentation_format=submission.presentation_format,
			is_active=True,
		)
		.order_by("-updated_at")
		.first()
	)
	if not rubric:
		raise Http404("No active rubric configured for this format.")

	rubric_items = list(rubric.items.all().order_by("sort_order", "id"))

	initial = {}
	existing_scores = {score.rubric_item_id: score for score in assignment.scores.all()}
	for item in rubric_items:
		if item.id in existing_scores:
			initial[f"item_{item.id}"] = int(existing_scores[item.id].value)
	if hasattr(assignment, "score_submission"):
		initial["comments"] = assignment.score_submission.comments

	if assignment.status == JudgeAssignment.STATUS_SUBMITTED and request.method == "GET":
		messages.warning(request, "This score is final and currently locked.")

	if request.method == "POST" and assignment.status == JudgeAssignment.STATUS_SUBMITTED:
		return HttpResponseForbidden("Score is locked. Organizer must reopen this assignment.")

	if request.method == "POST":
		form = ScoreSubmissionForm(request.POST, rubric_items=rubric_items)
		if form.is_valid():
			for item in rubric_items:
				Score.objects.update_or_create(
					assignment=assignment,
					rubric_item=item,
					defaults={"value": float(form.cleaned_data[f"item_{item.id}"])},
				)
			action = request.POST.get("action", "draft")
			is_final = action == "final"
			upsert_score_submission(
				assignment=assignment,
				comments=form.cleaned_data.get("comments", ""),
				is_final=is_final,
			)
			if is_final:
				messages.success(request, "Final score submitted.")
			else:
				messages.success(request, "Draft saved.")
			return redirect("judging:judge_dashboard", token=token)
	else:
		form = ScoreSubmissionForm(initial=initial, rubric_items=rubric_items)

	return render(
		request,
		"judging/score_submission.html",
		{
			"judge": judge,
			"assignment": assignment,
			"submission": submission,
			"rubric": rubric,
			"form": form,
			"rubric_items": rubric_items,
			"item_fields": [(item, form[f"item_{item.id}"]) for item in rubric_items],
		},
	)


def submission_qr_landing(request, submission_id):
	token = request.session.get("judge_token")
	if not token:
		messages.info(request, "Open your judge link first, then scan QR codes.")
		return redirect("judging:landing")

	judge = _get_judge_by_token(token)
	assignment = JudgeAssignment.objects.filter(judge=judge, submission_id=submission_id).first()
	if not assignment:
		return HttpResponseForbidden("You are not assigned to this submission.")
	return redirect("judging:score_submission", token=token, submission_id=submission_id)


def submission_qr_image(request, submission_id):
	submission = get_object_or_404(Submission, id=submission_id, is_active=True)
	qr_path = reverse("judging:submission_qr", args=[submission.id])
	qr_url = request.build_absolute_uri(qr_path)
	image = qrcode.make(qr_url, image_factory=qrcode.image.svg.SvgImage)
	data = image.to_string()
	return HttpResponse(data, content_type="image/svg+xml")


@login_required
def organizer_dashboard(request):
	event = Event.objects.filter(is_active=True).order_by("-date").first()
	if not event:
		return render(request, "judging/admin_dashboard.html", {"event": None})

	assignments = event.assignments.all()
	submissions = event.submissions.all().select_related("category", "presentation_format")
	rows = []
	for submission in submissions:
		sub_assignments = assignments.filter(submission=submission)
		completed = sub_assignments.filter(status=JudgeAssignment.STATUS_SUBMITTED).count()
		raw_values = [a.score_submission.raw_mean for a in sub_assignments if hasattr(a, "score_submission")]
		rows.append(
			{
				"submission": submission,
				"assigned_count": sub_assignments.count(),
				"completed_count": completed,
				"current_raw_mean": round(sum(raw_values) / len(raw_values), 3) if raw_values else 0,
			}
		)

	context = {
		"event": event,
		"submission_rows": rows,
		"judge_rows": judge_metrics(event),
		"submitted_assignments": assignments.filter(status=JudgeAssignment.STATUS_SUBMITTED)
		.select_related("judge", "submission")
		.order_by("-completed_at")[:20],
		"counts": {
			"submissions": event.submissions.count(),
			"judges": event.judges.count(),
			"assignments": assignments.count(),
			"completed": assignments.filter(status=JudgeAssignment.STATUS_SUBMITTED).count(),
		},
	}
	context["counts"]["missing"] = context["counts"]["assignments"] - context["counts"]["completed"]
	return render(request, "judging/admin_dashboard.html", context)


@login_required
def organizer_rankings(request):
	event = Event.objects.filter(is_active=True).order_by("-date").first()
	if not event:
		return render(request, "judging/rankings.html", {"event": None})

	category_id = request.GET.get("category")
	format_id = request.GET.get("format")
	rows = rankings_for_event(event, category_id=category_id, format_id=format_id)
	context = {
		"event": event,
		"rows": rows,
		"categories": event.categories.all(),
		"formats": {s.presentation_format for s in event.submissions.select_related("presentation_format")},
		"selected_category": int(category_id) if category_id and category_id.isdigit() else None,
		"selected_format": int(format_id) if format_id and format_id.isdigit() else None,
	}
	return render(request, "judging/rankings.html", context)


@login_required
def organizer_exports(request):
	event = Event.objects.filter(is_active=True).order_by("-date").first()
	return render(request, "judging/exports.html", {"event": event})


@login_required
def organizer_imports(request):
	event = Event.objects.filter(is_active=True).order_by("-date").first()
	if not event:
		return render(request, "judging/imports.html", {"event": None})

	if request.method == "POST":
		import_type = request.POST.get("import_type")
		form = CSVUploadForm(request.POST, request.FILES)
		if form.is_valid():
			csv_file = form.cleaned_data["csv_file"]
			if import_type == "submissions":
				created, updated = import_submissions(event, csv_file)
				messages.success(request, f"Submissions import complete. Created: {created}, updated: {updated}.")
			elif import_type == "judges":
				created, updated = import_judges(event, csv_file)
				messages.success(request, f"Judges import complete. Created: {created}, updated: {updated}.")
			elif import_type == "assignments":
				created, skipped = import_assignments(event, csv_file)
				messages.success(request, f"Assignments import complete. Created: {created}, skipped: {skipped}.")
			else:
				messages.error(request, "Unknown import type.")
			return redirect("judging:organizer_imports")
		messages.error(request, "Please upload a valid CSV file.")
	else:
		form = CSVUploadForm()

	return render(request, "judging/imports.html", {"event": event, "form": form})


@login_required
def export_csv(request, export_type):
	event = Event.objects.filter(is_active=True).order_by("-date").first()
	if not event:
		raise Http404("No active event.")

	export_map = {
		"raw": export_raw_scores,
		"adjusted": export_adjusted_rankings,
		"adjusted_xlsx": export_adjusted_rankings_xlsx,
		"judge_completion": export_judge_completion,
		"assignments": export_submission_assignments,
	}
	if export_type not in export_map:
		raise Http404("Unknown export type.")
	return export_map[export_type](event)


@login_required
def reopen_assignment(request, assignment_id):
	if request.method != "POST":
		return HttpResponseForbidden("POST required.")

	assignment = get_object_or_404(JudgeAssignment, id=assignment_id)
	assignment.status = JudgeAssignment.STATUS_REOPENED
	assignment.completed_at = None
	assignment.save(update_fields=["status", "completed_at", "updated_at"])

	if hasattr(assignment, "score_submission"):
		summary = assignment.score_submission
		summary.is_final = False
		summary.save(update_fields=["is_final", "updated_at"])

	messages.success(request, f"Reopened assignment for {assignment.judge.name} / {assignment.submission.abstract_number}.")
	return redirect("judging:organizer_dashboard")
