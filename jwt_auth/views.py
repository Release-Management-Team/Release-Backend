from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest

from members.models import Member

from .tokens import *
from .decorators import *
from .dto import *

from utils.decorators import use_body
from utils.encryption import checkpw

from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method='get',
    manual_parameters=validate_access_dto.request_param,
    responses={
        200: validate_access_dto.response_200,
    }
)
@api_view(['GET'])
@require_http_methods(['GET'])
@check_access_token
def validate_access(request, **kwargs):
    return JsonResponse({}, status=200)


@swagger_auto_schema(
    method='post',
    request_body= login_dto.request_body,
    responses={
        200: login_dto.response_200
    }
)
@api_view(['POST'])
@require_http_methods(['POST'])
@csrf_exempt
@use_body('id', 'password')
def login(request, body):
    id = body.get('id')
    pw = body.get('password')

    try: 
        member = Member.objects.get(id=id)
    except Member.DoesNotExist:
        return JsonResponse({'error': 'ERR_INVALID_ID'}, status=401) 

    decoded = member.password
    if not checkpw(pw, decoded): 
        return JsonResponse({'error': 'ERR_INVALID_PW'}, status=401) 

    access_token = create_access_token(member.id)
    refresh_token = create_refresh_token()

    return JsonResponse({
        'access_token': access_token, 
        'refresh_token': refresh_token
    })


@swagger_auto_schema(
    method='get',
    manual_parameters=refresh_token_dto.request_param,
    responses={
        200: refresh_token_dto.response_200,
    }
)
@api_view(['GET'])
@require_http_methods(['GET'])
@check_refresh_token
def refresh_token(request, **kwargs):
    old_access_token = request.headers.get('Access')[7:]

    if not old_access_token:
        return JsonResponse({'error': 'ERR_ACCESS_TOKEN_MISSING'}, status=401)
    
    try:
        payload = jwt.decode(old_access_token, settings.SECRET_KEY, algorithms='HS256')
    except:
        return JsonResponse({'error': 'ERR_INVALID_TOKEN'}, status=401)

    if payload['token_type'] != 'ACCESS':
        return JsonResponse({'error': 'ERR_WRONG_TOKEN'}, status=401)

    id = payload['id']
    
    try:
        member = Member.objects.get(id=id)
    except Member.DoesNotExist:
        return JsonResponse({'error': 'ERR_WRONG_ID'}, status=401)

    access_token = create_access_token(id)
    refresh_token = create_refresh_token()
    
    return JsonResponse({
        'access_token': access_token, 
        'refresh_token': refresh_token
    })