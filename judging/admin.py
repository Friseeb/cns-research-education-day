from django.contrib import admin

from .models import (
	Category,
	Event,
	Judge,
	JudgeAssignment,
	PresentationFormat,
	Rubric,
	RubricItem,
	Score,
	ScoreSubmission,
	Submission,
)


class RubricItemInline(admin.TabularInline):
	model = RubricItem
	extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	list_display = ("name", "date", "is_active")
	list_filter = ("is_active", "date")
	search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "event", "sort_order")
	list_filter = ("event",)
	ordering = ("event", "sort_order")


@admin.register(PresentationFormat)
class PresentationFormatAdmin(admin.ModelAdmin):
	list_display = ("name",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
	list_display = (
		"abstract_number",
		"title",
		"presenting_author",
		"category",
		"presentation_format",
		"is_active",
	)
	list_filter = ("event", "category", "presentation_format", "is_active")
	search_fields = ("abstract_number", "title", "presenting_author")


@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "event", "is_active")
	list_filter = ("event", "is_active")
	search_fields = ("name", "email")
	readonly_fields = ("token",)


@admin.register(JudgeAssignment)
class JudgeAssignmentAdmin(admin.ModelAdmin):
	list_display = ("judge", "submission", "status", "assigned_at", "completed_at")
	list_filter = ("event", "status")
	search_fields = ("judge__name", "submission__title", "submission__abstract_number")


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
	list_display = ("name", "event", "presentation_format", "is_active")
	list_filter = ("event", "presentation_format", "is_active")
	inlines = [RubricItemInline]


@admin.register(RubricItem)
class RubricItemAdmin(admin.ModelAdmin):
	list_display = ("label", "rubric", "min_score", "max_score", "weight", "sort_order")
	list_filter = ("rubric",)


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
	list_display = ("assignment", "rubric_item", "value", "updated_at")
	list_filter = ("assignment__event",)


@admin.register(ScoreSubmission)
class ScoreSubmissionAdmin(admin.ModelAdmin):
	list_display = ("assignment", "raw_mean", "is_final", "submitted_at")
	list_filter = ("assignment__event", "is_final")
