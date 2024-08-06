from django.urls import path
from . import views 

urlpatterns = [
    path('list', views.notices),
    path('upload-fcm-token', views.upload_fcm_token)
]