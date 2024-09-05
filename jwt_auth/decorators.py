from django.conf import settings
from django.http import JsonResponse

from members.models import Member

import jwt
import datetime
from functools import wraps


def check_access_token(func):
    """ 
    Check access token's validity    
    If token type is wrong or token was expired, returns http 403 response
    """

    @wraps(func)
    def decorated(request, *args, **kwargs):
        token = request.headers.get('Authorization')[7:]

        if not token:
            return JsonResponse({'error': 'ERR_ACCESS_TOKEN_MISSING'}, status=401)
        
        try:
           payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except:
            return JsonResponse({'error': 'ERR_INVALID_TOKEN'}, status=401)
        
        if payload['token_type'] != 'ACCESS' or payload['exp'] < int(datetime.datetime.now().timestamp()):
            return JsonResponse({'error': 'ERR_INVALID_TOKEN'}, status=401)

        return func(request, **kwargs)
    
    return decorated


def check_refresh_token(func):

    def decorated(request, *args, **kwargs):
        token = request.headers.get('X-Refresh_Token')

        if not token:
            return JsonResponse({'error': 'ERR_REFRESH_TOKEN_MISSING'}, status=401)
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except jwt.DecodeError:
            return JsonResponse({'error': 'ERR_INVALID_TOKEN'}, status=401)
        
        if payload['token_type'] != 'REFRESH':
            return JsonResponse({'error': 'ERR_WRONG_TOKEN'}, status=401)
        
        if payload['exp'] < int(datetime.datetime.now().timestamp()):
            return JsonResponse({'error': 'ERR_EXPIRED_TOKEN'}, status=401)

        return func(request, **kwargs)

    return decorated


def use_member(func):

    @wraps(func)
    def decorated(request, *args, **kwargs):
        token = request.headers.get('Authorization')[7:]
        id = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')['id']
        
        try:
            member = Member.objects.get(id=id)
        except Member.DoesNotExist:
            return JsonResponse({'error': 'ERR_MEMBER_DOES_NOT_EXIST'}, status=401)
        
        return func(request, member=member, *args, **kwargs)
    
    return decorated