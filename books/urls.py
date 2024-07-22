from django.urls import path

from . import views

urlpatterns = [
    path('book-list', views.book_list),
]