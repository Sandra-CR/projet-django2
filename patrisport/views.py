from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import SportSite

class SiteList(ListView):
  model = SportSite
  template_name = 'site_list.html'
  context_object_name = 'sites'
  paginate_by = 12

  def get_queryset(self):
    qs = SportSite.objects.all()
    query = self.request.GET.get("q", "").strip()
    if query:
      qs = qs.filter(
        Q(appellation__icontains=query)
        | Q(typologie__name__icontains=query)
        | Q(denomination__name__icontains=query)
      ).distinct()
    return qs

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["query"] = self.request.GET.get("q", "").strip()
    return context
