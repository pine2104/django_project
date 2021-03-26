from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Upload
from .forms import FileUpload
import numpy as np

class UploadView(CreateView):
    model = Upload
    fields = ['upload_file', ]
    template_name = 'uploader/upload_form.html'
    success_url = reverse_lazy('fileupload')  # back to url name: fileupload (in urls)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Upload.objects.all()
        return context
    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     if self.request.FILES:
    #         for f in self.request.FILES.getlist('file'):
    #             obj = self.model.objects.create(file=f)
    #     return super().form_valid(form)


@login_required
def upload_file(request):
    all_files = Upload.objects.all()
    if request.method == 'POST':
         form = FileUpload(request.POST, request.FILES)
         files = request.FILES.getlist('upload_file')
         if form.is_valid():
             for f in files:
                 file_instance = Upload(upload_file=f)
                 file_instance.save()
    else:
         form = FileUpload()

    return render(request, 'uploader/upload_files.html', {'form': form, 'all_files':all_files})



class FileDeleteView(LoginRequiredMixin, DeleteView):
    model = Upload
    success_url = reverse_lazy('fileupload')

