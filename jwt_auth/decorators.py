from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseBadRequest

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
            return HttpResponseForbidden()
        
        try:
           payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except:
            return HttpResponseForbidden()
        
        if payload['token_type'] == 'REFRESH' or payload['exp'] < int(datetime.datetime.now().timestamp()):
            return HttpResponseForbidden()

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