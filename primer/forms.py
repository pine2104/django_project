from django import forms
from .models import Primer

class PrimerForm(forms.ModelForm):
    class Meta:
        model = Primer
        fields = ['name', 'project','sequence', 'length', 'can_pcr', 'vector', 'modification', 'who_ordered', 'purpose', 'price', 'volumn', 'brand']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: p123'}),
            'sequence': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'without modification, ex: atccgaa'}),

            'modification': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': "ex: 5'bio, 14-idSp(abasic site at position-14, 5' = position-1)"}),
            'who_ordered': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: HWL'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: pcr 500 bp DNA for TPM'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: 1000'}),
            'volumn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: 100'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: IDT or MDBio'}),
        }
        labels = {
            'name': 'Primer name',
            'sequence': "Sequence (5' to 3')",
            'modification': 'Modification',
            'who_ordered': 'Who ordered',
            'purpose': 'Purpose',
            'price': 'Price (NT$)',
            'volumn': 'Volumn (uL, in 100 uM)',
            'brand': 'Produce Inc.',
        }



