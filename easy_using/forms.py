from mlpool.models import *
from django import forms


class UserRequestForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = [
            'binary_body',
            'model_name',
            'version',
            'description',
        ]