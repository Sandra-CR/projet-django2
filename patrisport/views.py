
from django.views.generic import ListView, DetailView
from .models import SportSite

class SiteList(ListView):
  model = SportSite
  template_name = 'site_list.html'
  context_object_name = 'sites'