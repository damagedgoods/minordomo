from django.contrib import admin

from .models import Message, Report, Variable

admin.site.register(Message)
admin.site.register(Report)
admin.site.register(Variable)