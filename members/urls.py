from django.urls import path

from . import views

urlpatterns = [
    path('home', views.home),
    path('profile', views.get_my_profile),
    path('profile/update', views.update_my_profile),
    path('change-password', views.change_password),
    path('member-list', views.get_members_list),
    path('member-profile', views.get_member_profile),
]