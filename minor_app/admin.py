from django.contrib import admin

from .models import Message, Report

admin.site.register(Message)
admin.site.register(Report)