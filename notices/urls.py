from django.urls import path
from . import views 

urlpatterns = [
    path("", views.notice_list),
    path("<int:notice_id>", views.notice_detail),
    path("important", views.get_important_notices),
]