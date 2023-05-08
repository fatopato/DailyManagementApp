# Generated by Django 4.2.1 on 2023-05-07 19:59

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Organization",
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
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Team",
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
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.organization",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TeamMember",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "teams",
                    models.ManyToManyField(related_name="members", to="core.team"),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("auth.user",),
            managers=[("objects", django.contrib.auth.models.UserManager()),],
        ),
        migrations.CreateModel(
            name="Daily",
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
                ("date", models.DateField()),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.team"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DailyItem",
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
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=100, null=True, unique=True
                    ),
                ),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("NS", "Not Started"),
                            ("BL", "Blocked"),
                            ("IP", "In Progress"),
                            ("CM", "Completed"),
                        ],
                        default="NS",
                        max_length=2,
                    ),
                ),
                ("progress_note", models.TextField(blank=True)),
                (
                    "daily",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.daily"
                    ),
                ),
                (
                    "team_member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.teammember",
                    ),
                ),
            ],
            options={"unique_together": {("daily", "team_member", "description")},},
        ),
    ]