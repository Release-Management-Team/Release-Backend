from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseNotFound

from members.models import Member

import jwt
import datetime

def check_access_token(func):
    """ 
    Check access token's validity    
    If token type is wrong or token was expired, returns http 403 response
    """

    def decorated(request, *args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return HttpResponseForbidden()
        
        try:
           payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except:
            return HttpResponseForbidden()
        
        if payload['token_type'] == 'REFRESH' or payload['exp'] < datetime.datetime.now():
            return HttpResponseForbidden()
        
        return func(request, payload, *args, **kwargs)
    
    return decorated



def use_member(func):
    def decorated(request, payload, *args, **kwargs):
        member = Member.objects.filter(id=payload['id'])

        return func(request, member, *args, **kwargs)
    
    return decorated
