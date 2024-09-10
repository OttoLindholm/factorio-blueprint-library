from django.views.generic import ListView

from bp_manager.models import Blueprint


class BlueprintListView(ListView):
    model = Blueprint
    context_object_name = "blueprint_list"
    template_name = "bp_manager/blueprint_list.html"
    queryset = Blueprint.objects.select_related("owner")
    paginate_by = 5
