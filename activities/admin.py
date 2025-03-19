from django.contrib import admin

from .models import Event, Activity

admin.site.register([Event, Activity])
