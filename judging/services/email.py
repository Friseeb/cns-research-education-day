"""
Email sending via SendGrid HTTP API.

Required env vars:
  SENDGRID_API_KEY  -- from sendgrid.com (free tier: 100 emails/day)
  MAIL_FROM         -- verified sender address
  MAIL_FROM_NAME    -- display name (default: "CNS Research Day 2026")
"""
import json
import urllib.request
import urllib.error

from django.conf import settings


def _sendgrid_send(to_email, to_name, subject, body_html, body_text):
    api_key = getattr(settings, "SENDGRID_API_KEY", "")
    from_email = getattr(settings, "MAIL_FROM", "")
    from_name = getattr(settings, "MAIL_FROM_NAME", "CNS Research Day 2026")

    if not api_key or not from_email:
        raise RuntimeError("SENDGRID_API_KEY and MAIL_FROM must be configured.")

    payload = json.dumps({
        "personalizations": [{"to": [{"email": to_email, "name": to_name}]}],
        "from": {"email": from_email, "name": from_name},
        "subject": subject,
        "content": [
            {"type": "text/plain", "value": body_text},
            {"type": "text/html", "value": body_html},
        ],
    }).encode()

    req = urllib.request.Request(
        "https://api.sendgrid.com/v3/mail/send",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=15)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"SendGrid error {exc.code}: {detail}") from exc


def send_judge_invite(judge, base_url):
    from judging.models import JudgeAssignment

    first = judge.name.split()[0] if judge.name else "Colleague"
    judge_url = f"{base_url.rstrip('/')}/judge/{judge.token}/"

    # Summarise what this judge is scoring
    assignments = sorted(
        JudgeAssignment.objects.filter(judge=judge)
        .select_related("submission", "submission__presentation_format"),
        key=lambda a: (
            0 if a.submission.abstract_number.startswith("PLAT") else 1,
            int(a.submission.abstract_number.split("-")[1]),
        ),
    )
    formats = {a.submission.presentation_format.name for a in assignments}
    is_oral = any("Oral" in f for f in formats)
    is_poster = any("Poster" in f for f in formats)

    if is_oral and not is_poster:
        session_desc = "oral platform presentations"
        rubric_items = [
            "Scientific question: clarity, relevance, importance",
            "Methods: design and analysis appropriateness",
            "Results: clarity and completeness",
            "Interpretation: conclusions supported by data",
            "Slide quality: readability and organisation",
            "Delivery: clarity and confidence",
            "Timing: appropriate use of time",
            "Response to questions: thoughtful answers",
            "Overall impression",
        ]
    elif is_poster and not is_oral:
        session_desc = "poster presentations"
        rubric_items = [
            "Scientific question: clarity, relevance, importance",
            "Methods: design and analysis appropriateness",
            "Results: clarity and completeness",
            "Interpretation: conclusions supported by data",
            "Poster design: readability and organisation",
            "Verbal explanation: clarity of presentation",
            "Response to questions: thoughtful answers",
            "Overall impression",
        ]
    else:
        session_desc = "presentations"
        rubric_items = [
            "Scientific question", "Methods", "Results", "Interpretation",
            "Presentation quality", "Response to questions", "Overall impression",
        ]

    n = len(assignments)
    assign_list_text = "\n".join(
        f"  • {a.submission.abstract_number} - {a.submission.presenting_author}: {a.submission.title}"
        for a in assignments
    )
    assign_list_html = "".join(
        f'<li style="margin-bottom:6px;"><strong>{a.submission.abstract_number}</strong> &mdash; '
        f'{a.submission.presenting_author}<br>'
        f'<span style="color:#555;font-size:0.88rem;">{a.submission.title}</span></li>'
        for a in assignments
    )
    rubric_text = "\n".join(f"  {i+1}. {item}" for i, item in enumerate(rubric_items))
    rubric_html = "".join(
        f'<li style="margin-bottom:4px;">{item}</li>' for item in rubric_items
    )

    subject = "CNS Research Day 2026 - Your Judging Portal"

    body_text = f"""Dear {first},

Thank you for agreeing to judge at the CNS Research & Education Innovation Day 2026 on June 9, 2026.

HOW TO ACCESS YOUR PORTAL
No login or password is required. Simply click your personal link on the day:

  {judge_url}

This link is unique to you - please do not share it. It works on any phone, tablet, or laptop.

YOUR ASSIGNMENTS ({n} {session_desc})
{assign_list_text}

SCORING
Each presentation is scored on {len(rubric_items)} criteria, each rated 1-5:

{rubric_text}

HOW IT WORKS
1. Open your portal link during or after each presentation.
2. Rate each criterion and add optional written comments.
3. Use "Save draft" to save progress, or "Submit final scores" when done.
   You can edit drafts at any time before the end of the session.
4. Please submit all scores before leaving at the end of your session.

If you have any questions, please reply to this email.

Best regards,
Sebastian Fridman, MD MPH
CNS Research Day 2026 Organizing Committee
"""

    body_html = f"""<div style="font-family:Arial,sans-serif;max-width:620px;margin:0 auto;color:#201436;">
<div style="background:linear-gradient(135deg,#201436,#4F2683);padding:24px 32px;border-radius:8px 8px 0 0;">
  <p style="color:#fff;font-size:1.2rem;font-weight:700;margin:0;">CNS Research &amp; Education Innovation Day 2026</p>
  <p style="color:rgba(255,255,255,0.7);font-size:0.85rem;margin:4px 0 0;">Department of Clinical Neurological Sciences &middot; Western University &middot; June 9, 2026</p>
</div>
<div style="background:#fff;padding:28px 32px;border:1px solid #dcdadf;border-top:0;border-radius:0 0 8px 8px;">
  <p>Dear {first},</p>
  <p>Thank you for agreeing to judge at the <strong>CNS Research &amp; Education Innovation Day 2026</strong>.</p>

  <h3 style="color:#4F2683;margin:24px 0 8px;">Your judging portal</h3>
  <p>No login or password is required &mdash; just click your personal link on the day. It works on any phone, tablet, or laptop.</p>
  <p style="margin:20px 0;text-align:center;">
    <a href="{judge_url}" style="background:#4F2683;color:#fff;padding:14px 28px;border-radius:8px;text-decoration:none;font-weight:600;font-size:1rem;">Open my judging portal</a>
  </p>
  <p style="font-size:0.82rem;color:#818284;text-align:center;">Or copy this link: <a href="{judge_url}" style="color:#4F2683;">{judge_url}</a></p>
  <p style="font-size:0.85rem;color:#818284;">This link is unique to you &mdash; please do not share it.</p>

  <h3 style="color:#4F2683;margin:24px 0 8px;">Your assignments &mdash; {n} {session_desc}</h3>
  <ol style="padding-left:1.2rem;margin:0 0 8px;">{assign_list_html}</ol>

  <h3 style="color:#4F2683;margin:24px 0 8px;">Scoring criteria (each rated 1-5)</h3>
  <ol style="padding-left:1.2rem;margin:0 0 8px;">{rubric_html}</ol>

  <h3 style="color:#4F2683;margin:24px 0 8px;">How it works</h3>
  <ol style="padding-left:1.2rem;">
    <li style="margin-bottom:6px;">Open your portal link during or after each presentation.</li>
    <li style="margin-bottom:6px;">Rate each criterion and add optional written comments.</li>
    <li style="margin-bottom:6px;">Use <strong>Save draft</strong> to save progress, or <strong>Submit final scores</strong> when done. Drafts can be edited at any time before the end of your session.</li>
    <li style="margin-bottom:6px;">Please submit all scores before leaving.</li>
  </ol>

  <p style="margin-top:24px;">If you have any questions, please reply to this email.</p>
  <p>Best regards,<br><strong>Sebastian Fridman, MD MPH</strong><br>CNS Research Day 2026 Organizing Committee</p>
</div>
</div>"""

    _sendgrid_send(judge.email, judge.name, subject, body_html, body_text)


def send_presenter_feedback(submission, base_url):
    """Send judging feedback to a presenter. Only sends if there are final scores."""
    from judging.models import JudgeAssignment

    final_assignments = list(
        JudgeAssignment.objects.filter(
            submission=submission,
            status=JudgeAssignment.STATUS_SUBMITTED,
            score_submission__is_final=True,
        ).select_related("score_submission")
    )
    if not final_assignments:
        return False

    comments = [
        a.score_submission.comments.strip()
        for a in final_assignments
        if hasattr(a, "score_submission") and a.score_submission.comments.strip()
    ]
    raw_scores = [a.score_submission.raw_mean for a in final_assignments if hasattr(a, "score_submission")]
    avg_score = round(sum(raw_scores) / len(raw_scores), 1) if raw_scores else None

    first = submission.presenting_author.split()[0] if submission.presenting_author else "Presenter"
    subject = f"CNS Research Day 2026 - Judging Feedback for #{submission.abstract_number}"

    score_line = f"Average score: {avg_score} / 5" if avg_score else ""

    comments_block_text = "\n".join(f"- {c}" for c in comments) if comments else "(No written comments were submitted.)"
    comments_block_html = "".join(
        f'<li style="margin-bottom:0.5rem;">{c}</li>' for c in comments
    ) if comments else "<li><em>No written comments were submitted.</em></li>"

    body_text = f"""Dear {first},

Thank you for your presentation at the CNS Research & Education Innovation Day 2026.

Below is the feedback from your judges for:
#{submission.abstract_number} - {submission.title}

{score_line}

Judge comments:
{comments_block_text}

Thank you again for your contribution to the day.

Best regards,
Sebastian Fridman, MD MPH
CNS Research Day 2026 Organizing Committee
"""

    body_html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;color:#201436;">
<div style="background:linear-gradient(135deg,#201436,#4F2683);padding:24px 32px;border-radius:8px 8px 0 0;">
  <p style="color:#fff;font-size:1.2rem;font-weight:700;margin:0;">CNS Research &amp; Education Innovation Day 2026</p>
  <p style="color:rgba(255,255,255,0.7);font-size:0.85rem;margin:4px 0 0;">Department of Clinical Neurological Sciences, Western University</p>
</div>
<div style="background:#ffffff;padding:28px 32px;border:1px solid #dcdadf;border-top:0;border-radius:0 0 8px 8px;">
  <p>Dear {first},</p>
  <p>Thank you for your presentation at the <strong>CNS Research &amp; Education Innovation Day 2026</strong>.</p>
  <p>Below is the feedback from your judges for:</p>
  <div style="background:#f5f4f8;border-left:4px solid #4F2683;padding:12px 16px;border-radius:0 8px 8px 0;margin:16px 0;">
    <strong>#{submission.abstract_number}</strong> - {submission.title}
    {"<br><span style='color:#4F2683;font-weight:600;margin-top:4px;display:block;'>" + score_line + "</span>" if score_line else ""}
  </div>
  <p><strong>Judge comments:</strong></p>
  <ul style="padding-left:1.2rem;margin:0 0 16px;">
    {comments_block_html}
  </ul>
  <p>Thank you again for your contribution to the day.</p>
  <p>Best regards,<br><strong>Sebastian Fridman, MD MPH</strong><br>CNS Research Day 2026 Organizing Committee</p>
</div>
</div>"""

    _sendgrid_send(
        submission.presenting_author_email if hasattr(submission, "presenting_author_email") else "",
        submission.presenting_author,
        subject,
        body_html,
        body_text,
    )
    return True


def send_judge_invites_bulk(event, base_url):
    """Send invites to all active judges. Returns (sent, failed) counts."""
    sent = 0
    failed = []
    for judge in event.judges.filter(is_active=True):
        try:
            send_judge_invite(judge, base_url)
            sent += 1
        except Exception as exc:
            failed.append(f"{judge.name} ({judge.email}): {exc}")
    return sent, failed


def send_feedback_bulk(event, base_url):
    """Send feedback to all scored presenters. Returns (sent, failed, skipped) counts."""
    sent = 0
    skipped = 0
    failed = []
    for submission in event.submissions.filter(is_active=True):
        if not submission.presenting_author_email:
            skipped += 1
            continue
        try:
            result = send_presenter_feedback(submission, base_url)
            if result:
                sent += 1
            else:
                skipped += 1
        except Exception as exc:
            failed.append(f"#{submission.abstract_number} {submission.presenting_author}: {exc}")
    return sent, failed, skipped
