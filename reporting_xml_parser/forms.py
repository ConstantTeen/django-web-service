from django import forms
from .models import *


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            'task',
            'chosen_model',
            'user_data',
        ]
