from django.urls import path
from . import views
from ideas.views import team_edit_idea

urlpatterns = [
    path("select-program/", views.select_program, name="select_program"),
    path("register/<int:program_id>/", views.register_idea, name="register_idea"),
    path("my-ideas/", views.my_ideas, name="my_ideas"),
    path("idea/<int:idea_id>/", views.idea_detail, name="idea_detail"),
    path("idea/<int:idea_id>/edit/", views.edit_idea, name="idea_edit"),
    path(
        "coordinator/review/",
        views.coordinator_review_ideas,
        name="coordinator_review_ideas",
    ),
    path(
        "coordinator/review/<int:idea_id>/",
        views.coordinator_review_idea,
        name="coordinator_review_idea",
    ),
    path(
        "committee/review/", views.committee_review_ideas, name="committee_review_ideas"
    ),
    path(
        "committee/review/<int:idea_id>/",
        views.committee_review_idea,
        name="committee_review_idea",
    ),
    path(
        "coordinator/assign_team/",
        views.coordinator_assign_team,
        name="coordinator_assign_team",
    ),
    path(
        "coordinator/assign_team/<int:idea_id>/",
        views.coordinator_assign_team_detail,
        name="coordinator_assign_team_detail",
    ),
    path("sponsor/review/", views.sponsor_review_list, name="sponsor_review_list"),
    path(
        "sponsor/review/<int:idea_id>/",
        views.sponsor_review_detail,
        name="sponsor_review_detail",
    ),
    path("coordinator/team/<int:team_id>/", views.team_detail, name="team_detail"),
    path("team/edit_idea/<int:idea_id>/", team_edit_idea, name="team_edit_idea"),
]
