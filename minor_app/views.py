from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Message
import json

def index(request):    
    messages = Message.objects.all().order_by('-date')
    p = Paginator(messages, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    

    template = loader.get_template("index.html")
    
    context = {
        "page_obj": page_obj
    }
    return HttpResponse(template.render(context, request))  

def message(request, message_id):    
    template = loader.get_template("message.html")
    message = Message.objects.get(pk=message_id)
    message.read_status = True
    message.save()
    context = {
        "message": message
    }
    return HttpResponse(template.render(context, request))
