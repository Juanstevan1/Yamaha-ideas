from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ideas", "0005_alter_idea_state"),
    ]

    operations = [
        migrations.AddField(
            model_name="program",
            name="committee_members",
            field=models.ManyToManyField(
                blank=True, related_name="committee_programs", to="auth.User"
            ),
        ),
    ]
