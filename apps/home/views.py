# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


@login_required(login_url="/login/")
def index(request):
    context = {}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def dashboard(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))









def icons(request):
    html_template = loader.get_template('home/icons.html')
    return HttpResponse(html_template.render({}, request))

def google(request):
    html_template = loader.get_template('home/map.html')
    return HttpResponse(html_template.render({}, request))

def profile(request):
    html_template = loader.get_template('home/profile.html')
    return HttpResponse(html_template.render({}, request))

def tables(request):
    html_template = loader.get_template('home/tables.html')
    return HttpResponse(html_template.render({}, request))

def login(request):
    html_template = loader.get_template('home/login.html')
    return HttpResponse(html_template.render({}, request))

def register(request):
    html_template = loader.get_template('home/register.html')
    return HttpResponse(html_template.render({}, request))
