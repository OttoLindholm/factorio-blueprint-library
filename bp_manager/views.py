from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)

from bp_manager.forms import (
    CommentaryForm,
    BlueprintForm,
    UserRegistrationForm,
    UserUpdateForm,
    UserDeleteForm,
    BlueprintSearchForm,
)
from bp_manager.models import Blueprint, Commentary, User, Like
from bp_manager.mixins import UserIsOwnerMixin


class BlueprintListView(ListView):
    model = Blueprint
    context_object_name = "blueprint_list"
    template_name = "bp_manager/blueprint_list.html"

    paginate_by = 8

    def get_queryset(self):
        queryset = Blueprint.objects.select_related("owner").prefetch_related(
            "tags", "comments"
        )
        query = self.request.GET.get("query", "")
        tag = self.request.GET.get("tag", "")

        if tag:
            queryset = queryset.filter(tags__name=tag).distinct()
        elif query:
            queryset = queryset.filter(
                Q(owner__username__icontains=query)
                | Q(title__icontains=query)
                | Q(tags__name__icontains=query)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        liked_blueprints = []

        if user.is_authenticated:
            liked_blueprints = Like.objects.filter(user=user).values_list(
                "blueprint_id", flat=True
            )

        context["search_form"] = BlueprintSearchForm(self.request.GET or None)
        context["liked_blueprints"] = liked_blueprints
        return context


class BlueprintDetailView(DetailView):
    model = Blueprint
    template_name = "bp_manager/blueprint_detail.html"
    context_object_name = "blueprint"
    queryset = Blueprint.objects.prefetch_related("tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commentary_form"] = CommentaryForm()
        context["comments"] = Commentary.objects.filter(
            blueprint=self.object
        ).select_related("user")
        return context


class BlueprintCreateView(LoginRequiredMixin, CreateView):
    model = Blueprint
    form_class = BlueprintForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class BlueprintUpdateView(
    LoginRequiredMixin,
    UserIsOwnerMixin,
    UpdateView,
):
    model = Blueprint
    form_class = BlueprintForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class BlueprintDeleteView(
    LoginRequiredMixin,
    UserIsOwnerMixin,
    DeleteView,
):
    model = Blueprint
    success_url = reverse_lazy("bp_manager:index")


class UserListView(ListView):
    model = User
    context_object_name = "user_list"
    template_name = "bp_manager/user_list.html"
    paginate_by = 10


class UserDetailView(DetailView):
    model = User
    template_name = "bp_manager/user_detail.html"
    context_object_name = "user"


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("bp_manager:user-login")


class UserUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = User
    form_class = UserUpdateForm

    def get_success_url(self):
        return self.object.get_absolute_url()


class UserDeleteView(LoginRequiredMixin, UserIsOwnerMixin, FormView):
    form_class = UserDeleteForm
    success_url = reverse_lazy("bp_manager:index")

    def form_valid(self, form):
        user = self.request.user
        if user.check_password(form.cleaned_data["password"]):
            user.delete()
            return super().form_valid(form)
        else:
            form.add_error("password", "Incorrect password")
            return self.form_invalid(form)


@login_required
def toggle_like(request, pk):
    blueprint = get_object_or_404(Blueprint, pk=pk)
    user = request.user
    like, created = Like.objects.get_or_create(blueprint=blueprint, user=user)
    if not created:
        like.delete()
    return redirect("bp_manager:index")


def add_comment(request, pk):
    blueprint = get_object_or_404(Blueprint, pk=pk)
    if request.method == "POST":
        form = CommentaryForm(request.POST)
        if form.is_valid():
            commentary = form.save(commit=False)
            commentary.user = request.user
            commentary.blueprint = blueprint
            commentary.save()
    return redirect("bp_manager:blueprint-detail", pk=blueprint.pk)
