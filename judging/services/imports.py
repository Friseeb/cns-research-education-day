import csv
from io import StringIO

from judging.models import Category, Judge, JudgeAssignment, PresentationFormat, Submission

_TRAINING_ALIASES = {
    "resident": "resident",
    "fellow": "fellow",
    "clinical fellow": "fellow",
    "research fellow": "fellow",
    "post-doc fellow": "fellow",
    "post-doc": "fellow",
    "postdoc": "fellow",
    "post doc": "fellow",
    "post-doctoral fellow": "fellow",
    "postdoctoral fellow": "fellow",
    "research associate": "fellow",
    "research assistant": "fellow",
    "student": "student",
    "medical student": "student",
    "undergraduate": "student",
    "undergraduate student": "student",
    "undergrad": "student",
    "graduate": "student",
    "graduate student": "student",
    "master's student": "student",
    "masters student": "student",
    "msc": "student",
    "phd": "student",
    "phd student": "student",
    "phd candidate": "student",
}


def _normalize_training_level(raw):
    return _TRAINING_ALIASES.get(raw.strip().lower(), "")


def _read_csv(uploaded_file):
    decoded = uploaded_file.read().decode("utf-8-sig")
    return csv.DictReader(StringIO(decoded))


def import_submissions(event, uploaded_file):
    created = 0
    updated = 0
    rows = _read_csv(uploaded_file)
    for row in rows:
        category_name = (row.get("category") or "").strip()
        format_name = (row.get("presentation_format") or "").strip()
        abstract_number = (row.get("abstract_number") or "").strip()
        if not category_name or not format_name or not abstract_number:
            continue

        category, _ = Category.objects.get_or_create(event=event, name=category_name)
        presentation_format, _ = PresentationFormat.objects.get_or_create(name=format_name)

        defaults = {
            "title": (row.get("title") or "").strip(),
            "presenting_author": (row.get("presenting_author") or "").strip(),
            "co_authors": (row.get("co_authors") or "").strip(),
            "category": category,
            "presentation_format": presentation_format,
            "training_level": _normalize_training_level(row.get("training_level") or ""),
            "abstract_text": (row.get("abstract_text") or "").strip(),
            "location": (row.get("location") or "").strip(),
        }
        submission, created_flag = Submission.objects.update_or_create(
            event=event,
            abstract_number=abstract_number,
            defaults=defaults,
        )
        if created_flag:
            created += 1
        else:
            updated += 1
    return created, updated


def import_judges(event, uploaded_file):
    created = 0
    updated = 0
    rows = _read_csv(uploaded_file)
    for row in rows:
        email = (row.get("email") or "").strip().lower()
        if not email:
            continue
        defaults = {
            "name": (row.get("name") or "").strip() or email,
            "affiliation": (row.get("affiliation") or "").strip(),
        }
        _, created_flag = Judge.objects.update_or_create(event=event, email=email, defaults=defaults)
        if created_flag:
            created += 1
        else:
            updated += 1
    return created, updated


def import_assignments(event, uploaded_file):
    created = 0
    skipped = 0
    rows = _read_csv(uploaded_file)
    for row in rows:
        email = (row.get("judge_email") or "").strip().lower()
        abstract_number = (row.get("abstract_number") or "").strip()
        if not email or not abstract_number:
            skipped += 1
            continue
        judge = Judge.objects.filter(event=event, email=email).first()
        submission = Submission.objects.filter(event=event, abstract_number=abstract_number).first()
        if not judge or not submission:
            skipped += 1
            continue
        _, created_flag = JudgeAssignment.objects.get_or_create(
            event=event,
            judge=judge,
            submission=submission,
        )
        if created_flag:
            created += 1
    return created, skipped
