from django.urls import path

from . import views

urlpatterns = [
    path('validate-access', views.validate_access),
    path('login', views.login),
    path('reissue-token', views.reissue_token),
]