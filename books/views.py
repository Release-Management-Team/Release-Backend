from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from members.models import Member
from .models import Book, BookRecord, BookTag, BookState

from jwt_auth.decorators import check_access_token, use_member
from utils.decorators import use_body, use_params


@require_http_methods(['GET'])
@check_access_token
def book_list(request: HttpRequest):
    data = [
        {
            'id': book.id,
            'title': book.title,
            'availability': book.availability,
            'author': book.author,
            'tags': [t.tag for t in book.tags.all()],
            'image': f'{settings.STORAGE_URL}/book-image/{book.id}' if book.image else ''
        }
        for book in Book.objects.all()
    ]
    return JsonResponse({'books': data})


@require_http_methods(['GET'])
@check_access_token
@use_params('id')
def book_info(request: HttpRequest, params: dict):
    book_id = params['id']

    try:
        book = Book.objects.get(id=book_id)
    except:
        return JsonResponse({'error': 'ERR_INVALID_BOOK_ID'}, status=400)
    
    data = {
        'id': book.id,
        'title': book.title,
        'availability': book.availability,
        'available_date': '',
        'author': book.author,
        'tags': [t.tag for t in book.tags.all()],
        'image': f'{settings.STORAGE_URL}/book-image/{book.id}' if book.image else ''
    }
    return JsonResponse(data)


@check_access_token
@use_member
@use_body('id', 'qrcode')
def borrow_book(request: HttpRequest, member: Member, body: dict):
    book_id = body['id']
    qrcode = body['qrcode']

    if qrcode != settings.QRCODE:
        return JsonResponse({'error': 'ERR_INVALID_QR'}, status=400)

    try:
        book = Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'ERR_INVALID_BOOK_ID'}, status=400)
    
    if book.availability != BookState.AVAILABLE:
        return JsonResponse({'error': 'ERR_UNABLE_TO_BORROW'}, status=400)

    book.availability = BookState.RENTED
    book.save()
    BookRecord.objects.create(borrower_id=member.id, book_id=book.id)

    return HttpResponse(status=200)

@require_http_methods(['POST'])
@use_member
@use_body('id', 'qrcode')
def return_book(request: HttpRequest, member: Member, body: dict):
    book_id = body['id']
    qrcode = body['qrcode']

    if qrcode != settings.QRCODE:
        return JsonResponse({'error': 'ERR_INVALID_QR'}, status=400)

    try:
        book = Book.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'ERR_INVALID_BOOK_ID'}, status=400)
    
    if book.availability != BookState.RENTED:
        return JsonResponse({'error': 'ERR_UNABLE_TO_RETURN'}, status=400)

    try:
        record = BookRecord.objects.get(borrower=member, book=book, actual_return=None)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'ERR_UNABLE_TO_RETURN'}, status=400)

    record.actual_return = timezone.now()
    record.save()

    book.availability = BookState.AVAILABLE
    book.save()

    return JsonResponse({})


@require_http_methods(['GET'])
@use_member
def borrowed_books(request: HttpRequest, member: Member):
    records = BookRecord.objects.filter(borrower=member, actual_return=None)

    data = { 
        'books': [
            {
                'id': record.book.id,
                'title': record.book.title,
                'availability': record.book.availability,
                'author': record.book.author,
                'tags': [t.tag for t in record.book.tags.all()],
                'image': record.book.image
            }
            for record in records
        ]
    }

    return JsonResponse(data)