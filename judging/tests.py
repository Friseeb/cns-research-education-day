from datetime import date
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from judging.models import (
	Category,
	Event,
	Judge,
	JudgeAssignment,
	PresentationFormat,
	Rubric,
	RubricItem,
	Score,
	Submission,
)
from judging.services.exports import export_raw_scores
from judging.services.scoring import calculate_raw_score, rankings_for_event, upsert_score_submission


class BaseFixture(TestCase):
	def setUp(self):
		self.event = Event.objects.create(name="CNS 2026", date=date(2026, 5, 14), is_active=True)
		self.category = Category.objects.create(event=self.event, name="Resident", sort_order=1)
		self.poster = PresentationFormat.objects.create(name="Poster presentation")
		self.rubric = Rubric.objects.create(
			event=self.event,
			name="Poster rubric",
			presentation_format=self.poster,
			is_active=True,
		)
		self.item1 = RubricItem.objects.create(rubric=self.rubric, label="Methods", sort_order=1, weight=1.0)
		self.item2 = RubricItem.objects.create(rubric=self.rubric, label="Results", sort_order=2, weight=2.0)
		self.submission = Submission.objects.create(
			event=self.event,
			abstract_number="A001",
			title="Test submission",
			presenting_author="Author",
			category=self.category,
			presentation_format=self.poster,
			abstract_text="Abstract",
		)
		self.submission2 = Submission.objects.create(
			event=self.event,
			abstract_number="A002",
			title="Test submission 2",
			presenting_author="Author 2",
			category=self.category,
			presentation_format=self.poster,
			abstract_text="Abstract 2",
		)
		self.judge = Judge.objects.create(
			event=self.event,
			name="Judge One",
			email="judge1@example.com",
		)
		self.assignment = JudgeAssignment.objects.create(
			event=self.event,
			judge=self.judge,
			submission=self.submission,
		)


class TokenTests(BaseFixture):
	def test_token_generation_unique(self):
		judge2 = Judge.objects.create(event=self.event, name="Judge Two", email="judge2@example.com")
		self.assertNotEqual(self.judge.token, judge2.token)
		self.assertGreaterEqual(len(self.judge.token), 24)


class PermissionTests(BaseFixture):
	def test_judge_can_only_access_assigned_submission(self):
		client = Client()
		allowed = reverse("judging:score_submission", args=[self.judge.token, self.submission.id])
		denied = reverse("judging:score_submission", args=[self.judge.token, self.submission2.id])
		self.assertEqual(client.get(allowed).status_code, 200)
		self.assertEqual(client.get(denied).status_code, 404)


class ScoringTests(BaseFixture):
	def test_raw_score_calculation(self):
		Score.objects.create(assignment=self.assignment, rubric_item=self.item1, value=3)
		Score.objects.create(assignment=self.assignment, rubric_item=self.item2, value=5)
		raw = calculate_raw_score(self.assignment)
		self.assertAlmostEqual(raw, (3 * 1 + 5 * 2) / 3)

	def test_adjusted_score_calculation(self):
		Score.objects.create(assignment=self.assignment, rubric_item=self.item1, value=3)
		Score.objects.create(assignment=self.assignment, rubric_item=self.item2, value=4)
		upsert_score_submission(self.assignment, is_final=True)

		judge2 = Judge.objects.create(event=self.event, name="Judge Two", email="judge2@example.com")
		assignment2 = JudgeAssignment.objects.create(event=self.event, judge=judge2, submission=self.submission)
		Score.objects.create(assignment=assignment2, rubric_item=self.item1, value=5)
		Score.objects.create(assignment=assignment2, rubric_item=self.item2, value=5)
		upsert_score_submission(assignment2, is_final=True)

		rankings = rankings_for_event(self.event)
		self.assertEqual(len(rankings), 1)
		self.assertIn("final_adjusted_score", rankings[0])


class RankingTests(BaseFixture):
	def test_rankings_by_category_and_format(self):
		judge2 = Judge.objects.create(event=self.event, name="Judge Two", email="judge2@example.com")
		assignment2 = JudgeAssignment.objects.create(event=self.event, judge=judge2, submission=self.submission)

		Score.objects.create(assignment=self.assignment, rubric_item=self.item1, value=4)
		Score.objects.create(assignment=self.assignment, rubric_item=self.item2, value=4)
		upsert_score_submission(self.assignment, is_final=True)

		Score.objects.create(assignment=assignment2, rubric_item=self.item1, value=5)
		Score.objects.create(assignment=assignment2, rubric_item=self.item2, value=5)
		upsert_score_submission(assignment2, is_final=True)

		rows = rankings_for_event(self.event, category_id=self.category.id, format_id=self.poster.id)
		self.assertEqual(len(rows), 1)
		self.assertEqual(rows[0]["submission"].id, self.submission.id)


class ExportTests(BaseFixture):
	def test_csv_export_generation(self):
		response = export_raw_scores(self.event)
		self.assertEqual(response.status_code, 200)
		self.assertIn("text/csv", response["Content-Type"])
		self.assertIn("raw_scores", response["Content-Disposition"])


class OrganizerFlowTests(BaseFixture):
	def setUp(self):
		super().setUp()
		self.user = User.objects.create_user(username="admin", password="pass1234")

	def test_reopen_assignment(self):
		Score.objects.create(assignment=self.assignment, rubric_item=self.item1, value=4)
		Score.objects.create(assignment=self.assignment, rubric_item=self.item2, value=4)
		upsert_score_submission(self.assignment, is_final=True)

		client = Client()
		client.force_login(self.user)
		url = reverse("judging:reopen_assignment", args=[self.assignment.id])
		response = client.post(url)
		self.assertEqual(response.status_code, 302)
		self.assignment.refresh_from_db()
		self.assertEqual(self.assignment.status, JudgeAssignment.STATUS_REOPENED)

	def test_qr_image_endpoint(self):
		url = reverse("judging:submission_qr_image", args=[self.submission.id])
		response = Client().get(url)
		self.assertEqual(response.status_code, 200)
		self.assertIn("image/svg+xml", response["Content-Type"])

	def test_import_submissions_view(self):
		client = Client()
		client.force_login(self.user)
		csv_data = (
			"abstract_number,title,presenting_author,co_authors,category,presentation_format,"
			"abstract_text,presentation_time,location\n"
			"A010,Imported Study,Import Author,Co A,Resident,Poster presentation,Text,,Board 10\n"
		)
		upload = SimpleUploadedFile("submissions.csv", csv_data.encode("utf-8"), content_type="text/csv")
		url = reverse("judging:organizer_imports")
		response = client.post(url, {"import_type": "submissions", "csv_file": upload})
		self.assertEqual(response.status_code, 302)
		self.assertTrue(Submission.objects.filter(event=self.event, abstract_number="A010").exists())

	def test_adjusted_xlsx_export(self):
		client = Client()
		client.force_login(self.user)
		url = reverse("judging:export_csv", args=["adjusted_xlsx"])
		response = client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertIn("spreadsheetml.sheet", response["Content-Type"])
