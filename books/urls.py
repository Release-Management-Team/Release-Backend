from django.urls import path

from . import views

urlpatterns = [
    path('list', views.book_list),
    path('info', views.book_info),
    path('borrow', views.borrow_book),
    path('return', views.return_book),
    path('borrowing', views.borrowed_books)
]