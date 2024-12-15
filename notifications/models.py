from django.db import models
from django.contrib.auth.models import User
from ideas.models import Idea


class Notification(models.Model):
    TYPES = (
        ("idea_update", "Idea Update"),
        ("team_assignment", "Team Assignment"),
        ("project_status", "Project Status"),
        ("general", "General"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    related_idea = models.ForeignKey(
        Idea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications",
    )
    type = models.CharField(max_length=20, choices=TYPES, default="general")
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification ({self.type}) for {self.user.username}"

    def mark_as_read(self):
        self.read = True
        self.save()
