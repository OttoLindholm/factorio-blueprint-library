from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from bp_manager.models import Blueprint


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
