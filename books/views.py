import json, datetime
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.views.decorators.http import require_http_methods

from members.models import Member
from .models import Book, BookRecord, BookTag

from jwt_auth.decorator import check_access_token, use_member
from utils.decorators import use_body

@require_http_methods(['GET'])
@check_access_token
def book_list(request: HttpRequest):
    data = [book.to_dict(['id', 'name', 'available', 'image']) for book in Book.objects.all()]
    return JsonResponse({'books': data})


@require_http_methods(['GET'])
@check_access_token
def book_info(request: HttpRequest):    
    book_id = request.GET.get('id')

    try:
        book = Book.objects.get(id=book_id)
    except:
        return HttpResponse(status=400)
    
    return JsonResponse(book.to_dict(['id', 'name', 'available', 'tags', 'donor', 'image']))


@require_http_methods(['POST'])
@check_access_token
@use_member
def borrow_book(request: HttpRequest, member: Member):
    body = json.loads(request.body)
    book_id = body['id']
    qrcode = body['qrcode']

    if qrcode != settings.QRCODE:
        return JsonResponse({'status': 1}, status=400)

    try:
        book = Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 0}, status=400)
    
    book.available=False
    book.save()
    BookRecord.objects.create(borrower_id=member.id, book_id=book.id, start_date=datetime.date.today())

    return HttpResponse(status=200)

@require_http_methods(['POST'])
@use_member
@use_body
def return_book(request: HttpRequest, member: Member, body: dict):
    book_id = body['id']
    qrcode = body['qrcode']

    if qrcode != settings.QRCODE:
        return JsonResponse({'status': 1}, status=400)

    try:
        book = Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 0}, status=400)
    
    if book.available:
        return HttpResponseBadRequest()

    records = BookRecord.objects.filter(borrower=member, book=book, actual_return=None)

    if len(records) == 0:
        return HttpResponseBadRequest()
    
    record = records[0]
    record.actual_return = datetime.date.today()
    record.save()

    book.available = True
    book.save()

    return HttpResponse(status=200)


@require_http_methods(['GET'])
@use_member
def borrowed_books(request: HttpRequest, member: Member):
    records = BookRecord.objects.filter(borrower=member, actual_return=None)

    data = { 
        'books': [
            {
                'id': record.book.id,
                'name': record.book.name,
                'author': record.book.author,
                'tags': [t.tag for t in record.book.tags.all()],
                'image': record.book.image,
            }
            for record in records
        ]
    }

    return JsonResponse(data)