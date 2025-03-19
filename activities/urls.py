from django.urls import path

from . import views

urlpatterns = [
    path('', views.activity_view),
    path('<int:activity_id>', views.activity_detail_view),
    path('study', views.study_view),
    path('project', views.project_view),
    path('event', views.event_view),
    path('event/<int:event_id>', views.event_detail_view)
]
