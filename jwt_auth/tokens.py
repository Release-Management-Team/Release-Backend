from django.conf import settings

import jwt
import datetime


def create_access_token(id):
    access_token = jwt.encode(
        {
            'id'    : id,
            'token_type'  : 'ACCESS', 
            'exp'   : datetime.datetime.now() + datetime.timedelta(days=int(settings.ACCESS_TOKEN_EXPIRE))
        },
        settings.SECRET_KEY,
        algorithm='HS256'
    )
    return access_token


def create_refresh_token():
    refresh_token = jwt.encode(
        {
            'token_type'  : 'REFRESH', 
            'exp'   : datetime.datetime.now() + datetime.timedelta(days=int(settings.REFRESH_TOKEN_EXPIRE))
        },
        settings.SECRET_KEY,
        algorithm='HS256'
    )
    return refresh_token
