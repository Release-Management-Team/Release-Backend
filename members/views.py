import re

from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.conf import settings

from .models import Member, Device
from notices.models import Notice
from activities.models import Event

from jwt_auth.decorators import *
from utils.decorators import *
from utils.encryption import hashpw, checkpw
from utils.storage import put_base64_image

from .dto import *
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method='get',
    manual_parameters=member_list_dto.request,
    responses={
        200: member_list_dto.response_200,
    }
)
@api_view(['GET'])
@require_http_methods(['GET'])
@check_access_token
def members_list(request: HttpRequest, **kwargs):
    profiles = [
        {
            "id": member.id,
            "name": member.name,
            "state": member.state,
            "role": member.role,
            "message": member.message,
            "image": f'{settings.STORAGE_URL}/member-image/{member.id}' if member.image else f'{settings.STORAGE_URL}/member-image/default'
        } for member in Member.objects.all()
    ]

    return JsonResponse({'profiles': profiles,}, safe=False, status=200)


@swagger_auto_schema(
    method='get',
    manual_parameters=member_profile_dto.request,
    responses={
        200: member_profile_dto.response_200,
    }
)
@api_view(['GET'])
@require_http_methods(['GET'])
@check_access_token
def member_profile(request: HttpRequest, student_id: int, **kwargs):
    try:
        member = Member.objects.get(id=student_id)
    except Member.DoesNotExist:
        return JsonResponse({'error': 'ERR_INVALID_MEMBER_ID'}, status=400)

    return JsonResponse({
        'id': member.id,
        'name': member.name,
        'state': member.state,
        'role': member.role,
        'message': member.message,
        'image': f'{settings.STORAGE_URL}/member-image/{member.id}' if member.image else f'{settings.STORAGE_URL}/member-image/default'
    }, status=200)


@swagger_auto_schema(
    method='get',
    manual_parameters=get_my_profile_dto.request,
    responses={200: get_my_profile_dto.response_200}
)
@swagger_auto_schema(
    method='put',
    request_body=update_my_profile_dto.request,
    responses={200: update_my_profile_dto.response_200}
)
@api_view(['GET', 'PUT'])
@require_http_methods(['GET', 'PUT'])
@check_access_token
@use_member
def my_profile(request: HttpRequest, member: Member, **kwargs):
    if request.method == 'GET':
        return get_my_profile(request, member)
    else:
        return update_my_profile(request, member=member, **kwargs)


@require_http_methods(['GET'])
def get_my_profile(request: HttpRequest, member: Member):
    return JsonResponse({
        'image': f'{settings.STORAGE_URL}/member-image/{member.id}' if member.image else f'{settings.STORAGE_URL}/member-image/default',
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


@use_body('phone', 'email', 'message', 'image')
def update_my_profile(request: HttpRequest, body: dict, **kwargs):
    member = kwargs['member']
    
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


@swagger_auto_schema(
    method='post',
    request_body=change_password_dto.request,
    responses={
        200: change_password_dto.response_200,
    }
)
@api_view(['POST'])
@require_http_methods(['POST'])
@check_access_token
@use_member
@use_body('old_password', 'new_password')
def change_password(request: HttpRequest, body: dict, member: Member, **kwargs):
    password = member.password
    old_password = body['old_password']
    new_password = body['new_password']

    if not checkpw(old_password, password):
        return JsonResponse({'error': 'ERR_INVALID_OLD_PW'}, status=400)
    
    if not (re.search('[a-zA-z]', new_password) and re.search('[0-9]', new_password) and 8 <= len(new_password) <= 20):
        return JsonResponse({'error': 'ERR_INVALID_PW_FORMAT'}, status=401)
    
    encoded = hashpw(new_password)
    member.password = encoded
    
    member.save()

    return JsonResponse({}, status=200)


@swagger_auto_schema(
    method='post',
    request_body=register_device_dto.request,
    responses={
        200: register_device_dto.response_200,
        201: register_device_dto.response_201,  
    }
)
@api_view(['POST'])
@require_http_methods(['POST'])
@check_access_token
@use_member
@use_body('uuid', 'fcm_token')
def register_device(request:HttpRequest, body: dict, member: Member, **kwargs):
    uuid = body['uuid']
    fcm_token = body['fcm_token']
 
    device, created = Device.objects.get_or_create(
        uuid=uuid,
        defaults={
            "fcm_token": fcm_token,
            "member": member
        }
    )
    
    if created:
        return JsonResponse({"uuid": str(device.uuid)}, status=201)
    else:
        return JsonResponse({"uuid": str(device.uuid)}, status=200)


@swagger_auto_schema(
    method='get',
    responses={
        200: "",
    }
)
@api_view(['GET'])
@require_http_methods(['GET'])
@check_access_token
@use_member
def home(request, member: Member, **kwargs):
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
