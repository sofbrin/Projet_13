from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


def index(request):
    """ Rendering home page """
    template = loader.get_template('content/index.html')
    return HttpResponse(template.render(request=request))


def contact(request):
    template = loader.get_template('content/contact.html')
    return HttpResponse(template.render(request=request))


def legal_notice(request):
    template = loader.get_template('content/legal_notice.html')
    return HttpResponse(template.render(request=request))
