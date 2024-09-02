import json
from django.http import HttpRequest, JsonResponse

from members.models import Member
from jwt_auth.decorators import check_access_token, use_member
from utils.decorators import use_body

@check_access_token
@use_member
@use_body('fcm_token')
def upload_fcm_token(request: HttpRequest, member: Member, body: dict):
    member.fcm_token = body['fcm_token']
    member.save()

    return JsonResponse({})