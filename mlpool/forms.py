from .models import *
from django import forms


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            'chosen_model',
            'user_data',
        ]
        labels = [
            ('chosen_model', 'asdasd'),
            ('user_data', 'asdasd'),
        ]
