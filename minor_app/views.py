from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

from .models import Message
import json

# Create your views here.
def index(request):    
    template = loader.get_template("index.html")
    messages = Message.objects.all()
    print(messages)
    context = {
        "messages": messages
    }
    return HttpResponse(template.render(context, request))  
