from django import forms
from django.forms import ClearableFileInput
from .models import Upload


class FileUpload(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['upload_file']
        widgets = {
            'upload_file': ClearableFileInput(attrs={'multiple': True}),
        }