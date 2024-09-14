from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from bp_manager.forms import (
    CommentaryForm,
    BlueprintForm,
    UserRegistrationForm,
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
    form_class = UserRegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("bp_manager:login")
