from django.shortcuts import render
from django.conf import settings

import jwt
import datetime


# 
#
#
def entry(request):
    return 0

#
#
#
def login(request):
    return 0

#
#
#
def refresh_token(request):
    return 0




def check_token(token):
    try:
        jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
    except jwt.exceptions.DecodeError:
        return False

    return True


def create_access_token(id):
    access_token = jwt.encode(
        {
            'id'    : id,
            'type'  : 'ACCESS', 
            'exp'   : datetime.datetime.now() + datetime.timedelta(days=settings.ACCESS_TOKEN_EXPIRE)
        },
        settings.SECRET_KEY,
        algorithm='HS256'
    )

    return access_token


def create_refresh_token(id):
    refresh_token = jwt.encode(
        {
            'id'    : id,
            'type'  : 'REFRESH', 
            'exp'   : datetime.datetime.now() + datetime.timedelta(days=settings.ACCESS_TOKEN_EXPIRE)
        },
        settings.SECRET_KEY,
        algorithm='HS256'
    )

    return refresh_token
    