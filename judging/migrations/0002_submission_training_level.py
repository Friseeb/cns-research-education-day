from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("judging", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="submission",
            name="training_level",
            field=models.CharField(
                blank=True,
                choices=[
                    ("resident", "Resident"),
                    ("fellow", "Clinical/Research/Post-doc Fellow"),
                    ("student", "Medical Student/Undergraduate/Graduate"),
                ],
                default="",
                max_length=20,
            ),
        ),
    ]
