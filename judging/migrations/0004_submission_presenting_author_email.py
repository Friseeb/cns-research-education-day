from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("judging", "0003_submission_award_eligible"),
    ]

    operations = [
        migrations.AddField(
            model_name="submission",
            name="presenting_author_email",
            field=models.EmailField(blank=True, default="", max_length=254),
        ),
    ]
