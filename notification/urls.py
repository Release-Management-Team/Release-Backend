from django.urls import path

from .views import upload_fcm_token

urlpatterns = [
    path('upload-fcm-token', upload_fcm_token)
]
