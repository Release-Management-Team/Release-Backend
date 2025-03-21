from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Event, Activity
from utils.decorators import use_body
from jwt_auth.decorators import check_access_token, use_member
from django.views.decorators.csrf import csrf_exempt

from .serializers import *
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='get',
    responses={200: get_activity_list_response_serializer}    
)
@api_view(['GET'])
@require_http_methods(['GET'])
@check_access_token
def activity_view(request: HttpRequest, **kwargs):
    return get_activity_list()


@csrf_exempt
@swagger_auto_schema(
    method='get',
    responses={200: get_activity_response_serializer}    
)
@swagger_auto_schema(
    method='patch',
    request_body=update_activity_serializer,
    responses={200: update_activity_response_serializer}    
)
@swagger_auto_schema(
    method='delete',
    responses={200: delete_activity_response_serializer}    
)
@api_view(['GET', 'PATCH', 'DELETE'])
@require_http_methods(['GET', 'PATCH', 'DELETE'])
@check_access_token
def activity_detail_view(request: HttpRequest, activity_id: int, **kwargs):
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        return JsonResponse({'message': 'given activity does not exist'}, status=400)
    
    if request.method == 'GET':
        return get_activity_detail(activity)
    elif request.method == 'PATCH':
        return update_activity(request, activity=activity, **kwargs)
    else:
        return delete_activity(activity)

@csrf_exempt
@swagger_auto_schema(
    method='post',
    request_body=create_activity_serializer,
    responses={200: create_activity_response_serializer}    
)
@api_view(['POST'])
@require_http_methods(['POST'])
@check_access_token
def project_view(request: HttpRequest, **kwargs):
    return create_activity(request, info=0, **kwargs)

@csrf_exempt
@swagger_auto_schema(
    method='post',
    request_body=create_activity_serializer,
    responses={200: create_activity_response_serializer}    
)
@api_view(['POST'])
@require_http_methods(['POST'])
@check_access_token
def study_view(request: HttpRequest, **kwargs):
    return create_activity(request, info=1, **kwargs)


def get_activity_list():
    activities = [
        {
            'id' : activity.id,
            'title': activity.title,
            'leader': activity.leader.name,
            'image': activity.image,
            'info': activity.info,
            'state': activity.state,
        }
        for activity in Activity.objects.all()
    ]
    return JsonResponse(activities, status=200, safe=False)


def get_activity_detail(activity: Activity):
    activity = {
        'id' : activity.id,
        'title': activity.title,
        'content': activity.content,
        'leader': activity.leader.name,
        'image': activity.image,
        'link': activity.link,
        'info': activity.info,
        'state': activity.state,
    }
    return JsonResponse(activity, status=200)

@use_member
@use_body('title', 'state', 'content', 'link')
def create_activity(reqeust, info: int, body, member, **kwargs):
    activity = Activity.objects.create(
        title = body['title'],
        content = body['content'],
        link = body['link'],
        leader = member,
        info = info,
        state = body['state'],
    )

    activity = {
        'id' : activity.id,
        'title': activity.title,
        'content': activity.content,
        'leader': activity.leader.name,
        'image': activity.image,
        'link': activity.link,
        'info': activity.info,
        'state': activity.state
    }

    return JsonResponse(activity, status=201)


@use_body('title', 'state', 'content', 'link')
def update_activity(request: HttpRequest, activity: Activity, body, **kwargs):
    activity.title = body.get('title')
    activity.state = body.get('state')
    activity.content = body.get('content')
    activity.link = body.get('link')
    activity.save()

    activity = {
        'id' : activity.id,
        'title': activity.title,
        'content': activity.content,
        'leader': activity.leader.name,
        'image': activity.image,
        'link': activity.link,
        'info': activity.info,
        'state': activity.state
    }

    return JsonResponse(activity, status=200)


def delete_activity(activity: Activity):
    activity.delete()

    return JsonResponse({'message': 'Activity'}, status=200)


#############################
#    From now, Events on    #
#############################


@swagger_auto_schema(
    method='get',
    responses={200: get_event_list_response_serializer}    
)
@swagger_auto_schema(
    method='post',
    request_body=create_event_serializer,
    responses={200: create_event_response_serializer}    
)
@api_view(['GET', 'POST'])
@require_http_methods(['GET', 'POST'])
@check_access_token
def event_view(request: HttpRequest, **kwargs):
    if request.method == 'GET':
        return get_event_list()
    else:
        return create_event(request)



@swagger_auto_schema(
    method='get',
    responses={200: get_event_response_serializer}    
)
@swagger_auto_schema(
    method='patch',
    request_body=update_event_serializer,
    responses={200: update_event_response_serializer}    
)
@swagger_auto_schema(
    method='delete',
    responses={200: delete_event_response_serializer}    
)
@api_view(['GET', 'PATCH', 'DELETE'])
@require_http_methods(['GET', 'PATCH', 'DELETE'])
@check_access_token
def event_detail_view(request: HttpRequest, event_id: int, **kwargs):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return JsonResponse({'message': 'given event does not exist'}, status=400)
    
    if request.method == 'GET':
        return get_event(event)
    elif request.method == 'PATCH':
        return update_event(request, event=event)
    else:
        return delete_event(event)


def get_event_list():
    events = [
        {
            'id': event.id,
            'title': event.title,
            'start_time': event.start_time.isoformat(),
            'place': event.place
        }
        for event in Event.objects.all()
    ]
    return JsonResponse(events, status=200, safe=False)


def get_event(event: Event):
    event = {
        'id': event.id,
        'title': event.title,
        'content': event.content,
        'start_time': event.start_time,
        'place': event.place
    }
    return JsonResponse(event, status=200)


@use_body('title', 'content', 'place', 'start_time')
def create_event(request: HttpRequest, body, **kwargs):
    event = Event.objects.create(
        title=body.get('title'),
        content=body.get('content'),
        place=body.get('place'),
        start_time= body.get('start_time')
    ) 

    event = {
        'id': event.id,
        'title': event.title,
        'content': event.content,
        'start_time': event.start_time,
        'place': event.place
    }
    return JsonResponse(event, status=201)


@use_body('title', 'content', 'place', 'start_time')
def update_event(request: HttpRequest, event: Event, body, **kwargs):
    event.title = body.get('title')
    event.content = body.get('content')
    event.place = body.get('place')
    event.start_time = body.get('start_time')
    event.save()

    event = {
        'id': event.id,
        'title': event.title,
        'content': event.content,
        'start_time': event.start_time,
        'place': event.place
    }
    return JsonResponse(event, status=200)


def delete_event(event: Event):
    event.delete()

    return JsonResponse({'message': 'event was deleted successfully'}, status=200)