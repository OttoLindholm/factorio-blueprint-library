from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from bp_manager.forms import CommentaryForm, BlueprintForm
from bp_manager.models import Blueprint, Commentary


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


class BlueprintUpdateView(LoginRequiredMixin, UpdateView):
    model = Blueprint
    form_class = BlueprintForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            return HttpResponseForbidden("You are not allowed to edit this object.")
        return obj

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class BlueprintDeleteView(LoginRequiredMixin, DeleteView):
    model = Blueprint
    success_url = reverse_lazy("bp_manager:index")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            return HttpResponseForbidden("You are not allowed to delete this object.")
        return obj
