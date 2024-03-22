from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Message, Report
import json

def index(request):    
    messages = Message.objects.all().order_by('-date')
    p = Paginator(messages, 10)
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

def message(request, slug):
    template = loader.get_template("message.html")
    message = Message.objects.get(slug=slug)
    message.read_status = True
    message.save()
    reports = Report.objects.filter(message=message)

    context = {
        "message": message,
        "reports": reports
    }
    return HttpResponse(template.render(context, request))
