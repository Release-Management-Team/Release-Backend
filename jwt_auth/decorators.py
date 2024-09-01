from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse

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
        token = request.headers.get('Authorization')

        if not token:
            return JsonResponse({'error': 'ACCESS_TOKEN_MISSING'}, status=401)
        
        try:
           payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except:
            return JsonResponse({'error': 'INVALID_TOKEN'}, status=401)
        
        if payload['token_type'] != 'ACCESS' or payload['exp'] < int(datetime.datetime.now().timestamp()):
            return JsonResponse({'error': 'INVALID_TOKEN'}, status=401)

        return func(request, **kwargs)
    
    return decorated

def check_refresh_token(func):

    def decorated(request, *args, **kwargs):
        token = request.headers.get('X-Refresh_Token')

        if not token:
            return JsonResponse({'error': 'REFRESH_TOKEN_MISSING'}, status=401)
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except jwt.DecodeError:
            return JsonResponse({'error': 'INVALID_TOKEN'})
        
        if payload['token_type'] != 'REFRESH':
            return JsonResponse({'error': 'WRONG_TOKEN'}, status=401)
        
        if payload['exp'] < int(datetime.datetime.now().timestamp()):
            return JsonResponse({'error': 'EXPIRED_TOKEN'}, status=401)

        return func(request, **kwargs)

    return decorated


def use_member(func):

    @wraps(func)
    def decorated(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        id = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')['id']
        member = Member.objects.get(id=id)
        return func(request, member=member, *args, **kwargs)
    
    return decorated