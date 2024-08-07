from django.urls import path

from . import views

urlpatterns = [
    path('studies', views.list_studies),
    path('projects', views.list_projects)
]
