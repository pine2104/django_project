from django import forms
from .models import Jcpaper
from bootstrap_datepicker_plus import DateTimePickerInput


# class DateTimeInput(forms.DateTimeInput):
#     input_type = "datetime-local"
#
#     def __init__(self, **kwargs):
#         kwargs["format"] = "%Y.%m.%dT%H:%M"
#         super().__init__(**kwargs)

# attrs={'type': 'date'}
class JCForm(forms.ModelForm):
    class Meta:
        model = Jcpaper
        fields = ['title', 'journal', 'hwl_recommend', 'presenter', 'file', 'location', 'time', 'link', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'journal': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder':'ex: PNAS'}),
            'location': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': "ex: B471"}),
            'time': DateTimePickerInput(),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'ex: https://... '}),
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What do you want to say....'}),
        }
        labels = {
            'title': 'Paper Title',
            'journal': "Journal",
            'hwl_recommend': "HWL recommend?",
            'location': 'Location',
            'time': 'Time',
            'link': 'URL link for paper',
            'content': 'Content',
        }



