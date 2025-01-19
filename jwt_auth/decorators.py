from django.conf import settings
from django.http import JsonResponse

from members.models import Member, Role

import jwt
import datetime
from functools import wraps


def check_access_token(func):
    """ 
    Check access token's validity    
    If token type is wrong or token was expired, returns http 403 response
    """

    @wraps(func)
    def decorated(request, **kwargs):
        if not 'Access' in request.headers:
            return JsonResponse({'error': 'ERR_MISSING_TOKEN'}, status=401)

        token = request.headers.get('Access')[7:]

        try:
           payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except:
            return JsonResponse({'error': 'ERR_INVALID_TOKEN'}, status=401)
        
        if payload['token_type'] != 'ACCESS' or payload['exp'] < int(datetime.datetime.now().timestamp()):
            return JsonResponse({'error': 'ERR_INVALID_TOKEN'}, status=401)

        return func(request, **kwargs, id=payload['id'])
    
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
    def decorated(request, **kwargs):
        try:
            member = Member.objects.get(id=kwargs['id'])
        except Member.DoesNotExist:
            return JsonResponse({'error': 'ERR_MEMBER_DOES_NOT_EXIST'}, status=401)
        
        return func(request,**kwargs, member=member)
    
    return decorated


def is_staff(func):
    @wraps(func)
    def decorator(request, **kwargs):
        id = kwargs['id']

        try:       
            member = Member.objects.get(id=id)
        except Member.DoesNotExist:
            return JsonResponse({}, status=404)

        if member.role != Role.STAFF:
            return JsonResponse(data={"error": "Need staff authority"},status=403)
        
        return func(request, **kwargs)

    return decorator 