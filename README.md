# CNS Research Day Judging Platform

Django MVP for judging poster and oral research presentations with token-based judge access, weighted rubrics, judge-level score normalization, organizer rankings, and CSV exports.

## Stack

- Backend: Django 4.2
- Database: PostgreSQL (production), SQLite (local default)
- UI: Django templates + mobile-first CSS
- Deployment: DigitalOcean App Platform

## Features implemented

- Event/category/format/submission/judge/assignment/rubric data model
- Unique URL-safe judge tokens
- Judge dashboard at `/judge/<token>/`
- Assignment scoring at `/judge/<token>/submission/<submission_id>/`
- Draft save and final submit (final locks assignment)
- QR landing route with judge-session authorization check
- Organizer dashboard `/organizer/`
- Rankings `/organizer/rankings/` with category + format filters
- CSV exports `/organizer/exports/`
- XLSX adjusted rankings export
- Organizer CSV imports `/organizer/imports/`
- Reopen action for submitted assignments from organizer dashboard
- QR image endpoint for posters `/submission/<id>/qr/image/`
- Scoring services:
  - Raw weighted mean
  - Judge median-centered adjustment
  - IQR normalization when judge has >= 4 completed assignments
- Seed command: `python manage.py seed_demo_event`
- Tests for token uniqueness, access control, scoring, rankings, exports
- Tests for reopen/import/QR/XLSX flows
- Production settings for WhiteNoise + `DATABASE_URL`

## Quickstart

1. Create virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

1. Run migrations:

```bash
python manage.py migrate
```

1. Seed demo event data:

```bash
python manage.py seed_demo_event
```

1. Create admin user:

```bash
python manage.py createsuperuser
```

1. Run server:

```bash
python manage.py runserver
```

## DigitalOcean deployment

1. Push this repository to GitHub.
1. In DigitalOcean App Platform, create app from GitHub repo.
1. Attach a Managed PostgreSQL database.
1. Set environment variables:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS`
   - `DATABASE_URL`
   - `CSRF_TRUSTED_ORIGINS`
1. Build command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

1. Run command:

```bash
gunicorn researchday.wsgi:application
```

## Notes

- Judges do not require user accounts; tokenized links are used.
- Admin and organizer pages require Django auth login.
- `X-Robots-Tag: noindex, nofollow` is added for privacy.
- `.env` is excluded from git.
