from .models import *
from django import forms


class MLModelForm(forms.ModelForm):
    class Meta:
        model = MLModel
        fields = [
            'binary_body',
            'model_name',
            'version',
            'description',
        ]
