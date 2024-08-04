from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from members.models import Member

from .tokens import *
from .decorator import *


@require_http_methods(['GET'])
@check_access_token
def validate_access(request):
    """
    Case: Client calls this view initially
    Require: access token
    Return: 200 response / 403 response    
    """

    return HttpResponse(200)



@require_http_methods(['POST'])
def login(request):
    """
    Case: both access, require token are invalid or expired
    Require: ID, password
    Return: New access token, refresh token / 401 response
    """

    id = request.POST.get('id')
    pw = request.POST.get('password')

    member = Member.objects.filter(id=id, password=pw)

    if not member:
        return HttpResponse('Unauthorized', status=401) 
   
    access_token = create_access_token(member['id'])
    refresh_token = create_refresh_token()

    return access_token, refresh_token


@require_http_methods(['GET'])
def refresh_token(request):
    """
    Case: Access token is invalid or expired
    Require: access token, refresh token 
    Return: New access, refresh token / 401 response
    """

    old_access_token = request.header.get('Authorization')
    old_refresh_token = request.header.get('X-Refresh_Token')

    if not old_access_token or not old_refresh_token:
        return HttpResponse('Unauthorized', status=401)
    
    if not ((check_token(old_access_token) == 0) and (check_token(old_refresh_token) == 1)):
        return HttpResponse('Unauthrized', status=401)

    id = get_id_from_access_token(old_access_token)
    if id == -1:
        return HttpResponseNotFound()

    access_token = create_access_token(id)
    refresh_token = create_refresh_token()
    
    return access_token, refresh_token