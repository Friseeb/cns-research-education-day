from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("judging", "0002_submission_training_level"),
    ]

    operations = [
        migrations.AddField(
            model_name="submission",
            name="award_eligible",
            field=models.BooleanField(default=True),
        ),
    ]
