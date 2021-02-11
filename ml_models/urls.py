from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'ml_models'

urlpatterns = [
    path('', views.index, name='index'),
]