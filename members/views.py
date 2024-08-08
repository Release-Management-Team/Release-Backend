import bcrypt

from django.http import HttpResponse, JsonResponse

from jwt_auth.decorators import *
from utils.decorators import *

@check_access_token
@use_member
def get_my_profile(request, member):
    return JsonResponse({
        'id': member.id,
        'name': member.name,
        'phone': member.phone,
        'email': member.email,
        'state': member.state,
        'role': member.role,
        'message': member.message,
        'image': member.image
    })



@check_access_token
@use_body
@use_member
def update_my_profile(request, body, member):
    try:
        if 'phone' in body:
            member.phone = body.get('phone')
        
        if 'email' in body:
            member.email = body.get('email')
        
        if 'message' in body:
            member.message = body.get('message')

        if 'image' in body:
            member.image = body.get('image')
    
        member.save()
    except KeyError:
        return HttpResponseBadRequest()
    finally:
        return HttpResponse(200)


@check_access_token
@use_body
@use_member
def change_password(request, body, member):
    try:
        pw = body.get('password')
        encoded = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
        member.password = encoded

        member.save()
    except:
        return HttpResponseBadRequest()
    finally:
        return HttpResponse(200)


@check_access_token
def get_members_list(request):
    profiles = Member.objects.values('id', 'name', 'state', 'role', 'message', 'image')    
    profiles_list = list(profiles)

    return JsonResponse({
        'profiles': profiles_list,
    }, safe=False)


@check_access_token
@use_body
def get_member_profile(request, body):
    id = body.get('id')

    try:
        member = Member.objects.get(id=id)
    except Member.DoesNotExist:
        return HttpResponseBadRequest()
    
    return JsonResponse({
        'id': member.id,
        'name': member.name,
        'state': member.state,
        'role': member.role,
        'message': member.message,
        'image': member.image
    })