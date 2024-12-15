from django.contrib import admin
from .models import Program, Idea, CommitteeRating, Team, SponsorDecision


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    filter_horizontal = ("committee_members",)


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ("title", "state", "creation_date", "employee", "program")
    list_filter = ("state", "creation_date", "program")
    search_fields = ("title", "description", "employee__username")


@admin.register(CommitteeRating)
class CommitteeRatingAdmin(admin.ModelAdmin):
    list_display = ("committee_member", "idea", "rating")
    search_fields = ("committee_member__username", "idea__title")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(SponsorDecision)
class SponsorDecisionAdmin(admin.ModelAdmin):
    list_display = ("idea", "sponsor", "decision", "decision_date")
    list_filter = ("decision", "decision_date")
    search_fields = ("idea__title", "sponsor__username")
