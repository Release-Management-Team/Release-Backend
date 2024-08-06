import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from members.models import Member
from .models import Notice

from jwt_auth.decorator import check_access_token, use_member

@check_access_token
def notices(request: HttpRequest):
    notices = [notice.to_json() for notice in Notice.objects.all()]
    return JsonResponse({"notices": notices})

@check_access_token
@use_member
def upload_fcm_token(request: HttpRequest, member: Member):
    body = json.loads(request.body)
    member.fcm_token = body['fcm_token']
    member.save()