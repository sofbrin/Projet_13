from django.urls import path
from . import views


urlpatterns = [
    path('legal_notice', views.legal_notice, name='legal_notice'),
]