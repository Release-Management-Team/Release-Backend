from django.urls import path

from . import views

urlpatterns = [
    path('', views.members_list),
    path('<int:student_id>', views.member_profile),
    path('register-device', views.register_device),
    path('my-profile', views.my_profile),
    path('my-profile/update', views.update_my_profile),
    path('my-profile/change-password', views.change_password),

    path('home', views.home),
]