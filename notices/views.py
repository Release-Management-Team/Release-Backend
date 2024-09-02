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
