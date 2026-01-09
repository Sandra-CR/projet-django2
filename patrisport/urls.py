from django.urls import path
from .views import SiteList

urlpatterns = [
    path('', SiteList.as_view(), name='article_list'),
]