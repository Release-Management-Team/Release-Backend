from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseBadRequest

import jwt
import datetime


# Check access token's validity
# If token type is wrong or token was expired, returns http 403 response
def check_access_token(func):
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

        return func(request, *args, **kwargs)

    return decorated



def create_access_token(id):
    access_token = jwt.encode(
        {
            'id'    : id,
            'token_type'  : 'ACCESS', 
            'exp'   : datetime.datetime.now() + datetime.timedelta(days=settings.ACCESS_TOKEN_EXPIRE)
        },
        settings.SECRET_KEY,
        algorithm='HS256'
    )
    return access_token



def create_refresh_token():
    refresh_token = jwt.encode(
        {
            'token_type'  : 'REFRESH', 
            'exp'   : datetime.datetime.now() + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE)
        },
        settings.SECRET_KEY,
        algorithm='HS256'
    )
    return refresh_token



def check_token(token):
    try:
       payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
    except:
        return -1
    
    if payload['token_type'] == 'ACCESS':
        return 0
    
    if payload['token_type'] == 'REFRESH':
        return 1
    
    return -1



def get_id_from_access_token(access_token):
    try:
        payload = jwt.decode(access_token. settings.SECRET_KEY, algorithms='HS256')
    except:
        return -1
    
    if payload['token_type'] != 'ACCESS':
        return -1
    
    return payload['id']