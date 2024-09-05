from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest

from members.models import Member

from .tokens import *
from .decorators import *

from utils.decorators import use_body
from utils.encryption import checkpw

@require_http_methods(['GET'])
@check_access_token
def validate_access(request):
    """
    Case: Client calls this view initially
    Require: access token
    Return: 200 response / 403 response    
    """

    return JsonResponse({}, status=200)



@require_http_methods(['POST'])
@csrf_exempt
@use_body('id', 'password')
def login(request, body):
    """
    Case: both access, require token are invalid or expired
    Require: ID, password
    Return: New access token, refresh token / 401 response
    """

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


@require_http_methods(['GET'])
@check_refresh_token
def refresh_token(request):
    """
    Case: Access token is invalid or expired
    Require: access token, refresh token 
    Return: New access, refresh token / 401 response
    """

    old_access_token = request.headers.get('Authorization')[7:]

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