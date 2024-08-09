from django.contrib import admin

from .models import Event, Study, Project

admin.site.register([Event, Study, Project])
