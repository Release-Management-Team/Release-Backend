
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from jwt_auth.decorators import *
from utils.decorators import *
from utils.encryption import hashpw


@require_http_methods(['GET'])
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


@require_http_methods(['POST'])
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


@require_http_methods(['POST'])
@check_access_token
@use_body
@use_member
def change_password(request, body, member):
    try:
        pw = body.get('password')
        encoded = hashpw(pw)
        member.password = encoded

        member.save()
    except:
        return HttpResponseBadRequest()
    finally:
        return HttpResponse(200)


@require_http_methods(['GET'])
@check_access_token
def get_members_list(request):
    profiles = Member.objects.values('id', 'name', 'state', 'role', 'message', 'image')    
    profiles_list = list(profiles)

    return JsonResponse({
        'profiles': profiles_list,
    }, safe=False)


@require_http_methods(['GET'])
@check_access_token
def get_member_profile(request):
    id = request.GET.get('id')

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