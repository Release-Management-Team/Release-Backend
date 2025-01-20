import json
from django.http import HttpRequest, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.http import require_http_methods

from .models import Notice

from jwt_auth.decorators import check_access_token, is_staff
from utils.decorators import use_body

@require_http_methods(["GET", "POST"])
@check_access_token
def notice_list(request: HttpRequest, **kwargs):
    if request.method == 'GET':
        return get_notice_list()
    else:
        return create_notice(request, id=kwargs['id'])


@require_http_methods(['GET', 'PUT', 'DELETE'])
@check_access_token
def notice_detail(request: HttpRequest, notice_id: int, **kwargs):
    if request.method == 'GET':
        return get_notice(notice_id)
    elif request.method == 'PUT':
        # return JsonResponse({}, status=400) 
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
    