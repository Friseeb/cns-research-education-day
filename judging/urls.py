from django.urls import path

from . import views

app_name = "judging"

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("judge/<str:token>/", views.judge_dashboard, name="judge_dashboard"),
    path(
        "judge/<str:token>/submission/<int:submission_id>/",
        views.score_submission,
        name="score_submission",
    ),
    path("submission/<int:submission_id>/qr/", views.submission_qr_landing, name="submission_qr"),
    path("submission/<int:submission_id>/qr/image/", views.submission_qr_image, name="submission_qr_image"),
    path("organizer/", views.organizer_dashboard, name="organizer_dashboard"),
    path("organizer/rankings/", views.organizer_rankings, name="organizer_rankings"),
    path("organizer/rankings/present/", views.organizer_rankings_present, name="organizer_rankings_present"),
    path("organizer/exports/", views.organizer_exports, name="organizer_exports"),
    path("organizer/exports/<str:export_type>/", views.export_csv, name="export_csv"),
    path("organizer/imports/", views.organizer_imports, name="organizer_imports"),
    path("organizer/assignment/<int:assignment_id>/reopen/", views.reopen_assignment, name="reopen_assignment"),
]
