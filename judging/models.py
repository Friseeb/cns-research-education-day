from django.db import models
from django.utils import timezone

from .services.tokens import generate_judge_token


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Event(TimeStampedModel):
	name = models.CharField(max_length=255)
	date = models.DateField()
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.name


class Category(TimeStampedModel):
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="categories")
	name = models.CharField(max_length=120)
	description = models.TextField(blank=True)
	sort_order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["sort_order", "name"]
		unique_together = ("event", "name")
		verbose_name_plural = "categories"

	def __str__(self):
		return f"{self.event.name} - {self.name}"


class PresentationFormat(models.Model):
	name = models.CharField(max_length=120, unique=True)
	description = models.TextField(blank=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name


class Submission(TimeStampedModel):
	TRAINING_RESIDENT = "resident"
	TRAINING_FELLOW = "fellow"
	TRAINING_STUDENT = "student"
	TRAINING_CHOICES = [
		(TRAINING_RESIDENT, "Resident"),
		(TRAINING_FELLOW, "Clinical/Research/Post-doc Fellow"),
		(TRAINING_STUDENT, "Medical Student/Undergraduate/Graduate"),
	]

	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="submissions")
	abstract_number = models.CharField(max_length=32)
	title = models.CharField(max_length=300)
	presenting_author = models.CharField(max_length=255)
	co_authors = models.TextField(blank=True)
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="submissions")
	presentation_format = models.ForeignKey(PresentationFormat, on_delete=models.PROTECT, related_name="submissions")
	training_level = models.CharField(max_length=20, choices=TRAINING_CHOICES, blank=True, default="")
	abstract_text = models.TextField()
	poster_file = models.FileField(upload_to="posters/", blank=True, null=True)
	presentation_time = models.DateTimeField(blank=True, null=True)
	location = models.CharField(max_length=255, blank=True)
	is_active = models.BooleanField(default=True)
	award_eligible = models.BooleanField(default=True)

	class Meta:
		ordering = ["abstract_number", "title"]
		unique_together = ("event", "abstract_number")

	def __str__(self):
		return f"#{self.abstract_number} - {self.title}"


class Judge(TimeStampedModel):
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="judges")
	name = models.CharField(max_length=255)
	email = models.EmailField()
	affiliation = models.CharField(max_length=255, blank=True)
	conflict_notes = models.TextField(blank=True)
	token = models.CharField(max_length=64, unique=True, db_index=True, editable=False)
	is_active = models.BooleanField(default=True)

	class Meta:
		unique_together = ("event", "email")
		ordering = ["name"]

	def save(self, *args, **kwargs):
		if not self.token:
			self.token = generate_judge_token()
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.name} ({self.event.name})"


class JudgeAssignment(TimeStampedModel):
	STATUS_NOT_STARTED = "not_started"
	STATUS_DRAFT = "draft"
	STATUS_SUBMITTED = "submitted"
	STATUS_REOPENED = "reopened"
	STATUS_CHOICES = [
		(STATUS_NOT_STARTED, "Not started"),
		(STATUS_DRAFT, "Draft"),
		(STATUS_SUBMITTED, "Submitted"),
		(STATUS_REOPENED, "Reopened"),
	]

	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="assignments")
	judge = models.ForeignKey(Judge, on_delete=models.CASCADE, related_name="assignments")
	submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="assignments")
	assigned_at = models.DateTimeField(default=timezone.now)
	completed_at = models.DateTimeField(blank=True, null=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NOT_STARTED)

	class Meta:
		unique_together = ("judge", "submission")
		ordering = ["submission__abstract_number"]

	def __str__(self):
		return f"{self.judge.name} -> {self.submission}"


class Rubric(TimeStampedModel):
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="rubrics")
	name = models.CharField(max_length=255)
	presentation_format = models.ForeignKey(PresentationFormat, on_delete=models.PROTECT, related_name="rubrics")
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return f"{self.name} ({self.presentation_format.name})"


class RubricItem(TimeStampedModel):
	rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE, related_name="items")
	label = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	min_score = models.PositiveSmallIntegerField(default=1)
	max_score = models.PositiveSmallIntegerField(default=5)
	weight = models.FloatField(default=1.0)
	sort_order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["sort_order", "id"]

	def __str__(self):
		return f"{self.rubric.name} - {self.label}"


class Score(TimeStampedModel):
	assignment = models.ForeignKey(JudgeAssignment, on_delete=models.CASCADE, related_name="scores")
	rubric_item = models.ForeignKey(RubricItem, on_delete=models.CASCADE, related_name="scores")
	value = models.FloatField()

	class Meta:
		unique_together = ("assignment", "rubric_item")

	def __str__(self):
		return f"{self.assignment_id} {self.rubric_item.label}={self.value}"


class ScoreSubmission(TimeStampedModel):
	assignment = models.OneToOneField(JudgeAssignment, on_delete=models.CASCADE, related_name="score_submission")
	raw_total = models.FloatField(default=0)
	raw_mean = models.FloatField(default=0)
	comments = models.TextField(blank=True)
	submitted_at = models.DateTimeField(blank=True, null=True)
	time_started = models.DateTimeField(blank=True, null=True)
	time_submitted = models.DateTimeField(blank=True, null=True)
	time_spent_seconds = models.PositiveIntegerField(default=0)
	is_final = models.BooleanField(default=False)

	def __str__(self):
		return f"Summary for assignment {self.assignment_id}"
