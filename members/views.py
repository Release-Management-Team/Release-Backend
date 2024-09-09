import re

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings

from jwt_auth.decorators import *
from utils.decorators import *
from utils.encryption import hashpw, checkpw
from utils.storage import put_base64_image

from notices.models import Notice
from activities.models import Event

@require_http_methods(['GET'])
@check_access_token
@use_member
def home(request, member: Member):
    notices = Notice.objects.filter(important=True, expired=False).order_by('date')
    notices_data = [
        {
            'title': notice.title,
            'content': notice.content
        }
        for notice in notices
    ]

    events = Event.objects.filter(this_week=True)
    schedules_data = [[] for _ in range(7)]

    for event in events:
        schedules_data[event.start_time.weekday()].append(
            {
                'name': event.name,
                'activity': '',
                'start_time': event.start_time.isoformat(),
                'end_time': event.end_time.isoformat() if event.end_time else ''
            }
        )

    data = {
        'name': member.name,
        'image': f'{settings.STORAGE_URL}/member-image/{member.id}' if member.image else '',
        'notices': notices_data,
        'schedules': schedules_data
    }

    return JsonResponse(data)

@require_http_methods(['GET'])
@check_access_token
@use_member
def get_my_profile(request, member):
    return JsonResponse({
        'image': f'{settings.STORAGE_URL}/member-image/{member.id}' if member.image else '',
        'name': member.name,
        'role': member.role,
        'message': member.message,
        'id': member.id,
        'department': member.department,
        'phone': member.phone,
        'email': member.email,
        'state': member.state,
        'joined_semester': member.joined_semester,
        'new': member.new,
    }, status=200)

@require_http_methods(['POST'])
@check_access_token
@use_body('phone', 'email', 'message', 'image')
@use_member
def update_my_profile(request, body, member):
    if body['phone'] != '':
        member.phone = body['phone']
    
    if body['email'] != '':
        member.email = body['email']
    
    if body['message'] != '':
        member.message = body['message']
    
    if body['image'] != '':
        put_base64_image('member-image', body['image'], str(member.id))
        member.image = True
    
    member.save()

    return JsonResponse({}, status=200)


@require_http_methods(['POST'])
@check_access_token
@use_body('old_password', 'new_password')
@use_member
def change_password(request, body, member):
    password = member.password
    old_password = body['old_password']
    
    if not checkpw(old_password, password):
        return JsonResponse({'error': 'ERR_INVALID_OLD_PW'}, status=400)
    
    new_password = body['new_password']

    if not (re.search('[a-zA-z]', new_password) and re.search('[0-9]', new_password) and 8 <= len(new_password) <= 20):
        return JsonResponse({'error': 'ERR_INVALID_PW_FORMAT'}, status=401)

    encoded = hashpw(new_password)
    member.password = encoded
    
    member.save()

    return JsonResponse({}, status=200)


@require_http_methods(['GET'])
@check_access_token
def get_members_list(request):
    profiles = Member.objects.values('id', 'name', 'state', 'role', 'message', 'image')    
    profiles_list = list(profiles)

    return JsonResponse({
        'profiles': profiles_list,
    }, safe=False, status=200)


@require_http_methods(['GET'])
@use_params('id')
@check_access_token
def get_member_profile(request, params):
    id = params['id']

    try:
        member = Member.objects.get(id=id)
    except Member.DoesNotExist:
        return JsonResponse({'error': 'ERR_INVALID_MEMBER_ID'}, status=400)

    return JsonResponse({
        'id': member.id,
        'name': member.name,
        'state': member.state,
        'role': member.role,
        'message': member.message,
        'image': member.image
    }, status=200)