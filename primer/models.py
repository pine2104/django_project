from django.db import models
from django.contrib.auth.models import User

from django import forms

# Create your models here.

class Vector(models.Model):
    name = models.CharField(max_length=50)
    sequence = models.CharField(max_length=20000)  # 5' to 3'
    def __str__(self):
        return f'{self.name}'

class Project(models.Model):
    name = models.CharField(max_length=50, default='TPM')
    def __str__(self):
        return f'{self.name}'

class Primer(models.Model):
    name = models.CharField(max_length=50)
    sequence = models.CharField(max_length=500) # 5' to 3'
    length = models.IntegerField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    can_pcr = models.BooleanField(default=True) # for pcr or not
    vector = models.ForeignKey(Vector, on_delete=models.CASCADE, default=1, related_name='vector')
    in_vector = models.BooleanField(default=True)
    dir = models.CharField(max_length=10, default='none')
    # position = models.CharField(max_length=10, default='none')
    position = models.IntegerField(default=-1)
    modification = models.CharField(max_length=200)
    who_ordered = models.CharField(max_length=50)
    purpose = models.CharField(max_length=200, blank = True)
    price = models.CharField(max_length=50, blank=True)
    volumn = models.CharField(max_length=50, blank=True) # conc. in 100 uM
    brand = models.CharField(max_length=50, blank=True) # which inc. produced
    created_at = models.DateTimeField(auto_now_add=True)
    edit_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by', default=1)
    edit_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edit_by', default=1)

class UploadPrimer(models.Model):
    excel_file = models.FileField() # .name, .size, .url, .open, .close, .save, .delete,
    excel_date = models.DateTimeField(auto_now_add =True)