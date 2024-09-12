from django.urls import path

from bp_manager.views import (
    BlueprintListView,
    BlueprintDetailView,
    BlueprintCreateView,
    BlueprintUpdateView,
    BlueprintDeleteView,
)

urlpatterns = [
    path("", BlueprintListView.as_view(), name="index"),
    path(
        "blueprints/<int:pk>/",
        BlueprintDetailView.as_view(),
        name="blueprint-detail"
    ),
    path(
        "blueprints/create/",
        BlueprintCreateView.as_view(),
        name="blueprint-create"
    ),
    path(
        "blueprints/<int:pk>/update/",
        BlueprintUpdateView.as_view(),
        name="blueprint-update"
    ),
    path(
        "blueprints/<int:pk>/delete/",
        BlueprintDeleteView.as_view(),
        name="blueprint-delete"
    ),
]

app_name = "bp_manager"
