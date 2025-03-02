import json
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Notice

from jwt_auth.decorators import check_access_token, is_staff
from utils.decorators import use_body

from .dto import *
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='get',
    manual_parameters=get_notice_list_dto.request_param,
    responses={200: get_notice_list_dto.response_200}    
)
@swagger_auto_schema(
    method='post',
    manual_parameters=create_notice_dto.request_param,
    request_body=create_notice_dto.request_body,
    responses={200: create_notice_dto.response_200}
)
@api_view(['GET', 'POST'])
@require_http_methods(["GET", "POST"])
@check_access_token
def notice_list(request: HttpRequest, **kwargs):
    if request.method == 'GET':
        return get_notice_list()
    else:
        return create_notice(request, id=kwargs['id'])



@swagger_auto_schema(
    method='get',
    manual_parameters=get_notice_dto.request_param,
    responses={200: get_notice_dto.response_200}
)
@swagger_auto_schema(
    method='put',
    manual_parameters=update_notice_dto.request_param,
    request_body=update_notice_dto.request_body,
    responses={200: update_notice_dto.response_200}
)
@swagger_auto_schema(
    method='delete',
    manual_parameters=delete_notice_dto.request_param,
    responses={200: delete_notice_dto.response_200}
)
@api_view(['GET', 'PUT', 'DELETE'])
@require_http_methods(['GET', 'PUT', 'DELETE'])
@check_access_token
def notice_detail(request: HttpRequest, notice_id: int, **kwargs):
    if request.method == 'GET':
        return get_notice(notice_id)
    elif request.method == 'PUT':
        return update_notice(request, notice_id=notice_id, **kwargs)
    else:
        return delete_notice(request, notice_id=notice_id, **kwargs)
    

def get_notice_list():
    notices = [
        {
            "id": notice.id,
            'title': notice.title,
            'content': notice.content,
            'date': notice.date,
            'important': notice.important,
            'expired': notice.expired,
        } for notice in Notice.objects.all()
    ]
    return JsonResponse({"notices": notices})


@is_staff
@use_body('title', 'content', 'important')
def create_notice(request, id, body, **kwargs):
    notice = Notice.objects.create(
        title = body['title'],
        content = body['content'],
        important = body['important']
    )

    notice = {
        "id": notice.id,
        "title": notice.title,
        "content": notice.content,
        "date": notice.date,
        "important": notice.important,
        "expired": notice.expired    
    }

    return JsonResponse({"notice": notice}, status=200)


def get_notice(notice_id: int):
    try:
        notice = Notice.objects.get(id=notice_id)
    except Notice.DoesNotExist:
        return JsonResponse({}, status=404)

    notice_json = {
        "id": notice.id,
        "title": notice.title,
        "content": notice.content,
        "date": notice.date,
        "important": notice.important,
        "expired": notice.expired    
    }

    return JsonResponse({'notice': notice_json}, status=200)


@is_staff
@use_body('title', 'content', 'important', 'expired')
def update_notice(request:HttpRequest, body, **kwargs):
    try:
        notice = Notice.objects.get(id=kwargs['notice_id'])
    except Notice.DoesNotExist:
        return JsonResponse({}, status=404)
    
    notice.title = body['title']
    notice.content = body['content']
    notice.important = body['important']
    notice.expired = body['expired']
    notice.save()

    notice_json = {
        "id": notice.id,
        "title": notice.title,
        "content": notice.content,
        "date": notice.date,
        "important": notice.important,
        "expired": notice.expired    
    }
    
    return JsonResponse({'notice': notice_json}, status=200)


@is_staff
def delete_notice(request, **kwargs):
    try:
        notice = Notice.objects.get(id=kwargs['notice_id'])
    except Notice.DoesNotExist:
        return JsonResponse({}, status=404)
    
    notice.delete()

    return JsonResponse({}, status=200)


@swagger_auto_schema(
    method='get',
    manual_parameters=get_important_notice_list_dto.request_param,
    responses={200: get_important_notice_list_dto.response_200}    
)
@api_view(['GET'])
@check_access_token
def get_important_notices(request, **kwargs):
    notices = [
        {
            "id": notice.id,
            'title': notice.title,
        } for notice in Notice.objects.filter(important=True, expired=False)
    ]
    return JsonResponse({"notices": notices})