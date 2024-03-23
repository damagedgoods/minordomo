from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Message, Report
import json

def index(request):    

    # Ordering and filtering
    categoryFilter = request.GET.get('categoryFilter')
    orderSelection = request.GET.get('orderSelection')    
    if categoryFilter is None: categoryFilter = "0"
    if orderSelection is None: orderSelection = "0"
    ordering = "-date"
    if (int(orderSelection) == 1):
        ordering = "text"
        
    if (int(categoryFilter) == 2):
        messages = Message.objects.filter(category=Message.Category.CONCEPT).order_by(ordering)
    elif (int(categoryFilter) == 3):
        messages = Message.objects.filter(category=Message.Category.MUSIC).order_by(ordering)
    else:
        messages = Message.objects.all().order_by(ordering)

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
        "page_obj": page_obj,
        "orderSelection": orderSelection,
        "categoryFilter": categoryFilter,
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
        "reports": reports,        
    }
    return HttpResponse(template.render(context, request))
