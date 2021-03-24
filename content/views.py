from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


def index(request):
    """ Rendering home page """
    page_title = {"page_title": "Accueil"}
    return render(request, 'content/index.html', page_title)


def legal_notice(request):
    page_title = {"page_title": "Mentions légales"}
    return render(request, 'content/legal_notice.html', page_title)
