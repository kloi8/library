from django import forms
from .models import Material
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title','author','discipline','school_class','file']
