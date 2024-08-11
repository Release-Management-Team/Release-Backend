import json
from django.http import HttpRequest, HttpResponse, JsonResponse

from members.models import Member
from .models import Notice

from jwt_auth.decorators import check_access_token, use_member

@check_access_token
def notices(request: HttpRequest):
    notices = [
        {
            'title': notice.title,
            'content': notice.content,
            'date': str(notice.date)
        }
        for notice in Notice.objects.all()
    ]
    return JsonResponse({"notices": notices})

@check_access_token
@use_member
def upload_fcm_token(request: HttpRequest, member: Member):
    body = json.loads(request.body)
    member.fcm_token = body['fcm_token']
    member.save()

    return HttpResponse(status=200)