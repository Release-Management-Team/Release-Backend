import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.http import require_http_methods
# from pkg_resources import require

from .models import Book, BookRecord, BookTag

@require_http_methods(['GET'])
def book_list(request: HttpRequest):
    data = [book.to_json(['id', 'name', 'available', 'image']) for book in Book.objects.all()]
    return JsonResponse({'books': data})

@require_http_methods(['GET'])
def book_info(request: HttpRequest):
    body = json.loads(request.body)
    
    book_id = body['id']
    books = Book.objects.filter(id=book_id)
    
    if books.count != 1:
        return HttpResponse(status=400)
    
    return JsonResponse(books[0].to_json(['id', 'name', 'available', 'tags', 'donor', 'image']))

@require_http_methods(['POST'])
def borrow_book(request: HttpRequest):
    pass

@require_http_methods(['POST'])
def return_book(request: HttpRequest):
    pass

@require_http_methods(['GET'])
def borrowed_books(request: HttpRequest):
    pass