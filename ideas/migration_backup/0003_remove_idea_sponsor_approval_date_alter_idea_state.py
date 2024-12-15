# Generated by Django 5.1.4 on 2024-12-12 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ideas", "0002_idea_extra_data_idea_prototype_file_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="idea",
            name="sponsor_approval_date",
        ),
        migrations.AlterField(
            model_name="idea",
            name="state",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("reviewed_by_coordinator", "Reviewed by Coordinator"),
                    ("committee_in_review", "Under Committee Review"),
                    ("committee_approved", "Approved by Committee"),
                    ("committee_rejected", "Rejected by Committee"),
                    ("in_progress", "In Progress"),
                    ("completed", "Completed"),
                ],
                default="pending",
                max_length=30,
            ),
        ),
    ]
