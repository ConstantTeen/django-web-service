from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'mlpool'

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.projects, name='projects'),
    path('project/<int:project_id>', views.project, name='project'),
    path('task/<int:task_id>', views.task, name='task'),
    path('new_request/<int:task_id>', views.new_request, name='new_request'),
    path('request/<int:request_id>', views.request, name='request'),
    # path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]