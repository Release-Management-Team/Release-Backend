from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Event, Study, Project
from members.models import Member

from jwt_auth.decorators import check_access_token, use_member
from utils.decorators import use_body

@require_http_methods(['GET'])
@check_access_token
def list_studies_projects(request: HttpRequest):
    studies = [
        {
            'type': 'study',
            'name': study.name,
            'description': study.description,
            'tags': [t.tag for t in study.tags.all()],
            'state': study.state,
        }
        for study in Study.objects.all()
    ]
    
    projects = [
        {
            'type': 'project',
            'name': project.name,
            'description': project.description,
            'tags': [t.tag for t in project.tags.all()],
            'state': project.state,
        }
        for project in Project.objects.all()
    ]

    data = {
        'activities': studies + projects
    }
    return JsonResponse(data)

@require_http_methods(['GET'])
@check_access_token
def list_event(request: HttpRequest):
    events = [
        {
            'name': event.name,
            'start_time': event.start_time.isoformat(),
            'end_time': event.end_time.isoformat(),
            'place': event.place
        }
        for event in Event.objects.all()
    ]

    data = {
        'events': events
    }

    return JsonResponse(data)
