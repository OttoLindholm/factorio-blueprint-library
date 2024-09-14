from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
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
    UserAuthenticationForm,
    UserUpdateForm,
    UserDeleteForm,
)
from bp_manager.models import Blueprint, Commentary, User
from bp_manager.mixins import UserIsOwnerMixin


class BlueprintListView(ListView):
    model = Blueprint
    context_object_name = "blueprint_list"
    template_name = "bp_manager/blueprint_list.html"
    queryset = Blueprint.objects.select_related("owner")
    paginate_by = 6


class BlueprintDetailView(LoginRequiredMixin, DetailView):
    model = Blueprint
    template_name = "bp_manager/post_detail.html"
    context_object_name = "blueprint"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentaryForm()
        context["comments"] = Commentary.objects.filter(blueprint=self.object)
        return context

    def post(self, request, *args, **kwargs):
        blueprint = self.get_object()
        form = CommentaryForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.blueprint = blueprint
            comment.user = self.request.user
            comment.save()
            return redirect("blog:post-detail", pk=blueprint.pk)

        context = self.get_context_data(object=blueprint)
        context["form"] = form
        return self.render_to_response(context)


class BlueprintCreateView(LoginRequiredMixin, CreateView):
    model = Blueprint
    form_class = BlueprintForm

    def form_valid(self, form):
        form.instance.user = self.request.user
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
    success_url = reverse_lazy("bp_manager:login")


class UserLoginView(LoginView):
    model = User
    form_class = UserAuthenticationForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("bp_manager:index")


class UserUpdateView(
    LoginRequiredMixin,
    UserIsOwnerMixin,
    UpdateView
):
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
