from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.response_request, name='response_request'),
]