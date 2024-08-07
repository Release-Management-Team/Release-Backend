from django.contrib import admin

from .models import Study, Project

admin.site.register([Study, Project])
