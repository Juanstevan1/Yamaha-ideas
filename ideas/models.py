from django.db import models
from django.contrib.auth.models import User


class Program(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    coordinators = models.ManyToManyField(
        User, related_name="coordinated_programs", blank=True
    )
    form_config = models.JSONField(
        blank=True, null=True
    )  # Define campos adicionales para ideas.
    committee_members = models.ManyToManyField(
        User, related_name="committee_programs", blank=True
    )

    def __str__(self):
        return self.name


class Idea(models.Model):
    STATES = (
        ("pending", "Pending"),
        ("reviewed_by_coordinator", "Reviewed by Coordinator"),
        ("coordinator_rejected", "Rejected by Coordinator"),  # Nuevo estado
        ("committee_in_review", "Under Committee Review"),
        ("committee_approved", "Approved by Committee"),
        ("committee_rejected", "Rejected by Committee"),
        ("sponsor_rejected", "Rejected by Sponsor"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("adjustments_required_by_sponsor", "Adjustments Required by Sponsor"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    state = models.CharField(max_length=50, choices=STATES, default="pending")
    creation_date = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="proposed_ideas"
    )
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="ideas", null=True, blank=True
    )
    coordinator_review_comments = models.TextField(blank=True, null=True)
    committee_feedback = models.TextField(blank=True, null=True)
    committee_rating = models.FloatField(null=True, blank=True)
    sponsor_adjustment_comments = models.TextField(blank=True, null=True)
    assigned_team = models.ManyToManyField(
        User, related_name="team_assigned_ideas", blank=True
    )
    extra_data = models.JSONField(blank=True, null=True)
    prototype_file = models.FileField(upload_to="prototypes/", blank=True, null=True)
    related_image = models.ImageField(upload_to="images/", blank=True, null=True)

    def calculate_committee_decision(self):
        """Calcula la decisión final del comité basada en las calificaciones."""
        total_votes = self.ratings.count()
        approved_votes = self.ratings.filter(
            rating__gte=3
        ).count()  # Asumiendo que una calificación >= 3 es una aprobación
        rejected_votes = total_votes - approved_votes

        if approved_votes > rejected_votes:
            return "committee_approved"
        else:
            return "committee_rejected"

    def all_committee_reviews_complete(self):
        """Verifica si todos los miembros del comité han evaluado la idea"""
        return self.ratings.count() >= self.program.committee_members.count()


class CommitteeRating(models.Model):
    committee_member = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="given_ratings"
    )
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="ratings")
    rating = models.FloatField()
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Rating by {self.committee_member.username} for {self.idea.title}"


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User, related_name="teams")
    idea = models.OneToOneField(
        Idea, on_delete=models.CASCADE, related_name="team", null=True, blank=True
    )

    def __str__(self):
        return self.name


class SponsorDecision(models.Model):
    idea = models.OneToOneField(
        Idea,
        on_delete=models.CASCADE,
        related_name="sponsor_decision_entry",  # Cambiado para evitar conflicto
    )
    sponsor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sponsor_decisions",
    )
    decision = models.CharField(
        max_length=20,
        choices=(
            ("approved", "Approved"),
            ("rejected", "Rejected"),
            ("adjustments_required", "Adjustments Required"),
        ),
    )
    comments = models.TextField(blank=True, null=True)
    decision_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sponsor Decision for {self.idea.title} by {self.sponsor.username}"
