from .models import Primer
import django_filters
from django import forms
from django_filters.widgets import RangeWidget



class PrimerFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    sequence = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    modification = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    purpose = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    position = django_filters.RangeFilter()

    class Meta:
        model = Primer
        fields = '__all__'

