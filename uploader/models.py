from django.db import models

# Create your models here.

class Upload(models.Model):
    upload_file = models.FileField() # .name, .size, .url, .open, .close, .save, .delete,
    upload_date = models.DateTimeField(auto_now_add =True)
