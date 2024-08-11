from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from .models import Event, Study, Project
from members.models import Member

from jwt_auth.decorators import check_access_token, use_member
from utils.decorators import use_body

@require_GET
@check_access_token
def list_studies(request: HttpRequest):
    data = {
        'studies': [
            {
                'name': study.name,
                'description': study.description,
                'tags': [t.tag for t in study.tags.all()],
                'leader': study.leader.id,
                'members': [m.id for m in study.members.all()],
            }
            for study in Study.objects.all()
        ] 
    }
    return JsonResponse(data)

@require_GET
@check_access_token
def list_projects(request: HttpRequest):
    data = {
        'projects': [
            {
                'name': project.name,
                'description' :project.description,
                'leader': project.leader.id,
                'members': [m.id for m in project.members.all()]
            }
            for project in Project.objects.all()
        ] 
    }
    return JsonResponse(data)
