from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'xml'

urlpatterns = [
    path('', views.index, name='index'),
    path('new_request/<int:project_id>', views.new_request, name='new_request'),
    # path('task/<int:task_id>', views.task, name='task'),
    path('user_request/<int:request_id>', views.user_request, name='user_request'),
    # path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]