from django.urls import path

from . import views

urlpatterns = [
    path('', views.book_list),
    path('<int:book_id>', views.book_info),
    path('<int:book_id>/borrow', views.borrow_book),
    path('<int:book_id>/return', views.return_book),
    path('borrowing', views.borrowed_books)
]