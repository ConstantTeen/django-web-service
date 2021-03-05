from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'easy_using'

urlpatterns = [
    path('', views.index, name='index'),
    path('new_request/', views.new_request, name='new_request'),
    path('new_response/', views.new_response, name='new_response'),
]