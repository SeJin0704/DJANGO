# Generated by Django 4.1.7 on 2023-03-22 05:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Board",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("context", models.TextField()),
                ("writer", models.CharField(max_length=10)),
                ("input_date", models.DateTimeField(default=django.utils.timezone.now)),
                ("view_count", models.IntegerField(default=0)),
            ],
        ),
    ]