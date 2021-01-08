from django.shortcuts import render

# Create your views here.
# from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Upload
import numpy as np

class UploadView(CreateView):
    model = Upload
    fields = ['upload_file', ]
    success_url = reverse_lazy('fileupload')  # back to url name: fileupload (in urls)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Upload.objects.all()
        return context



class FileDeleteView(DeleteView):
    model = Upload
    success_url = reverse_lazy('fileupload')

