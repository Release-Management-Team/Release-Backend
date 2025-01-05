from django.urls import path

from . import views

urlpatterns = [
    path('/', views.get_members_list),
    path('/<int:student_id>', views.get_member_profile),
    path('/my-profile', views.get_my_profile),
    path('/change-password', views.change_password),

    path('home', views.home),
]