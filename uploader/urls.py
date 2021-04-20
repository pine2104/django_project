from . import views as uploader_views
from django.urls import path



urlpatterns = [

    path('fileupload/', uploader_views.upload_file, name='fileupload'),
    path('delete/<int:pk>/', uploader_views.FileDeleteView.as_view(), name='delete'),

]