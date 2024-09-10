from django.urls import path

from bp_manager.views import BlueprintListView, BlueprintDetailView

urlpatterns = [
    path("", BlueprintListView.as_view(), name="index"),
    path("blueprints/<int:pk>/", BlueprintDetailView.as_view(), name="blueprint-detail"),
]

app_name = "bp_manager"
