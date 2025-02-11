from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from members.models import Member
from .models import Book, BookRecord, BookTag, BookState

from jwt_auth.decorators import check_access_token, use_member
from utils.decorators import use_body

from .dto import *
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method='GET',
    manual_parameters=get_book_list_dto.request_param,
    responses={
        200: get_book_list_dto.response_200
    }
)
@api_view(['GET'])
@require_http_methods(['GET'])
@check_access_token
def book_list(request: HttpRequest, id: int):
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
    return JsonResponse({'books': data}, status=200)

    
@swagger_auto_schema(        
    method='GET',
    manual_parameters=get_book_detail_dto.request_param,
    responses={
        200: get_book_detail_dto.response_200,
    }
)
@api_view(['GET'])
@require_http_methods(['GET'])
@check_access_token
def book_info(request: HttpRequest, id: int, book_id: int):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'ERR_INVALID_BOOK_ID'}, status=400)
    
    data = {
        'id': book.id,
        'title': book.title,
        'availability': book.availability,
        'author': book.author,
        'tags': [t.tag for t in book.tags.all()],
        'image': f'{settings.STORAGE_URL}/book-image/{book.id}' if book.image else ''
    }
    return JsonResponse(data, status=200)


@swagger_auto_schema(
    method='POST',
    manual_parameters=borrow_book_dto.request_param,
    request_body=borrow_book_dto.request_body,
    responses={
        200: borrow_book_dto.response_200,
    }
)
@api_view(['POST'])
@require_http_methods(['POST'])
@check_access_token
@use_member
@use_body('qrcode')
def borrow_book(request: HttpRequest, book_id: int, member:Member, body: dict, **kwargs):
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

    return JsonResponse({}, status=200)


@swagger_auto_schema(
    method='POST',
    manual_parameters=return_book_dto.request_param,
    request_body=return_book_dto.request_body,
    responses={
        200: return_book_dto.response_200,
    }
)
@api_view(['POST'])
@require_http_methods(['POST'])
@check_access_token
@use_member
@use_body('qrcode')
def return_book(request: HttpRequest, book_id: int, member: Member, body: dict, **kwargs):    
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

    return JsonResponse({}, status=200)


@swagger_auto_schema(
    method='GET',
    manual_parameters=get_borrowed_books_dto.request_param,
    responses={
        200: get_borrowed_books_dto.response_200
    }
)
@api_view(['GET'])
@require_http_methods(['GET'])
@check_access_token
@use_member
def borrowed_books(request: HttpRequest, id, member: Member):
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

    return JsonResponse(data, status=200)