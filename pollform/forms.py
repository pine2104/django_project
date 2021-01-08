from django import forms
from .models import Questions

class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['question', 'choices']

        # labels = {
        #     'name': 'Primer name',
        #     'sequence': "Sequence (5' to 3')",
        #     'modification': 'Modification',
        #     'who_ordered': 'Who ordered',
        #     'purpose': 'Purpose',
        #     'price': 'Price (NT$)',
        #     'volumn': 'Volumn (uL, in 100 uM)',
        #     'brand': 'Produce Inc.',
        # }



