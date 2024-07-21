from django.http import HttpRequest, JsonResponse
from django.core import serializers
from django.views.decorators.http import require_http_methods

from .models import Book, BookRecord, BookTag

@require_http_methods(["GET"])
def list_books(request: HttpRequest):
    data = serializers.serialize('python', Book.objects.all(), fields=['id', 'name', 'available', 'tags', 'image'])
    return JsonResponse({'books': data})
