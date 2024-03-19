from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Message
import json

def index(request):    
    template = loader.get_template("index.html")
    messages = Message.objects.all().order_by('-date')
    context = {
        "messages": messages
    }
    return HttpResponse(template.render(context, request))  

def message(request, message_id):    
    template = loader.get_template("message.html")
    message = Message.objects.get(pk=message_id)
    context = {
        "message": message
    }
    return HttpResponse(template.render(context, request))
