from django.contrib import admin
from .models import Book, BookRecord, BookTag

admin.site.register([Book, BookRecord, BookTag])
