from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from .models import Event, Study, Project
from members.models import Member

from jwt_auth.decorators import check_access_token, use_member
from utils.decorators import use_body

@require_GET
@check_access_token
def list_studies(request: HttpRequest):
    data = {'studies': [study.to_dict(['name', 'description', 'tags', 'leader', 'members']) for study in Study.objects.all()] }
    return JsonResponse(data)

@require_GET
@check_access_token
def list_projects(request: HttpRequest):
    data = {'projects': [project.to_dict(['name', 'description', 'leader', 'members']) for project in Project.objects.all()] }
    return JsonResponse(data)
