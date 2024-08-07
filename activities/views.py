from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET

from .models import Study, Project

from jwt_auth.decorator import check_access_token

@require_GET
@check_access_token
def list_studies(request:HttpRequest):
    data = {'studies': [study.to_dict(['name', 'president', 'members', 'goal', 'description']) for study in Study.objects.all()] }
    return JsonResponse(data)

