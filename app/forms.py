from django import forms
from app.models import PedagogicalResource

class PedagogicalResourceForm(forms.ModelForm):
    class Meta:
        model = PedagogicalResource
        fields = ['title', 'description', 'file']
