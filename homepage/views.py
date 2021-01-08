from django.shortcuts import render
from django.views.generic.base import TemplateView, View
# Create your views here.


class homeview(TemplateView):
    template_name = 'homepage/homepage.html'