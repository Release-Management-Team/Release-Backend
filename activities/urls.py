from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_studies_projects),
    path('event', views.list_event)
]
