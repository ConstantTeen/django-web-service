from django.contrib import admin
from .models import *

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(MLModel)
admin.site.register(UserRequest)
admin.site.register(Result)
admin.site.register(Response)
