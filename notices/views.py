from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from .models import Notice

def notices(request: HttpRequest):
    notices = [notice.to_json() for notice in Notice.objects.all()]
    return JsonResponse({"notices": notices})