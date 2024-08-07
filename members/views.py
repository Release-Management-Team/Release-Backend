from django.http import JsonResponse

from jwt_auth.decorators import *
from utils.decorators import *
# Create your views here.

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
    pass



@check_access_token
@use_body
@use_member
def change_password(request):
    pass



@check_access_token
def get_members_list(request):
    profiles = Member.objects.values('id', 'name', 'state', 'role', 'message', 'image')    
    profiles_list = list(profiles)

    return JsonResponse({
        'profiles': profiles_list,
    }, safe=False)


@check_access_token
@use_body
def get_member_profile(request):
    pass