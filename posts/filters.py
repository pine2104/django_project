from .models import Post, Jcpaper
import django_filters
from django import forms
from django_filters.widgets import RangeWidget

class PostFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    content = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    date_posted = django_filters.DateFromToRangeFilter(
        field_name="date_posted",
        lookup_expr='gte',
        widget=RangeWidget(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'author', 'date_posted']

class JCFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    journal = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    hwl_recommend = django_filters.BooleanFilter()

    content = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    date_posted = django_filters.DateFromToRangeFilter(
        field_name="date_posted",
        lookup_expr='gte',
        widget=RangeWidget(attrs={'type': 'date'})
    )

    class Meta:
        model = Jcpaper
        fields = ['title', 'journal', 'hwl_recommend', 'content', 'presenter', 'date_posted']