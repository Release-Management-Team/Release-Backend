from django.urls import path

from . import views

urlpatterns = [
    path('book-list', views.list_books),
]