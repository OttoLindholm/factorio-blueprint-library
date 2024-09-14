from django.urls import path

from bp_manager.views import (
    BlueprintListView,
    BlueprintDetailView,
    BlueprintCreateView,
    BlueprintUpdateView,
    BlueprintDeleteView,
    UserListView,
    UserDetailView,
    UserRegisterView,
    UserUpdateView,
    UserDeleteView,
    UserLoginView,
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
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/login/", UserLoginView.as_view(), name="user-login"),
    path(
        "uers/<int:pk>/", UserDetailView.as_view(), name="user-detail"
    ),
    path("users/register/", UserRegisterView.as_view(), name="user-register"),
    path(
        "users/<int:pk>/update/",
        UserUpdateView.as_view(),
        name="user-update",
    ),
    path(
        "users/<int:pk>/delete/",
        UserDeleteView.as_view(),
        name="user-delete",
    ),
]

app_name = "bp_manager"
