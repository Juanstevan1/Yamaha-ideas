# Generated by Django 5.1.4 on 2024-12-14 22:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idea',
            name='sponsor_approval_date',
        ),
        migrations.AddField(
            model_name='idea',
            name='extra_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='idea',
            name='prototype_file',
            field=models.FileField(blank=True, null=True, upload_to='prototypes/'),
        ),
        migrations.AddField(
            model_name='idea',
            name='related_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='idea',
            name='sponsor_adjustment_comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='program',
            name='committee_members',
            field=models.ManyToManyField(blank=True, related_name='committee_programs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='program',
            name='form_config',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='idea',
            name='state',
            field=models.CharField(choices=[('pending', 'Pending'), ('reviewed_by_coordinator', 'Reviewed by Coordinator'), ('coordinator_rejected', 'Rejected by Coordinator'), ('committee_in_review', 'Under Committee Review'), ('committee_approved', 'Approved by Committee'), ('committee_rejected', 'Rejected by Committee'), ('sponsor_rejected', 'Rejected by Sponsor'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('adjustments_required_by_sponsor', 'Adjustments Required by Sponsor')], default='pending', max_length=50),
        ),
    ]
