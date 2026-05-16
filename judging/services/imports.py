import csv
from io import StringIO

from judging.models import Category, Judge, JudgeAssignment, PresentationFormat, Submission


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
