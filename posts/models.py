from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
def make_file_path(instance, filename):
   pid = instance.category
   path = f'protocols/{pid}/{filename}'
   return path

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey('Category', related_name='Project', null=True, on_delete=models.CASCADE)
    file = models.FileField(upload_to=make_file_path, blank=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('postdetail', kwargs={'pk': self.pk})

    # def get_upload_to(self, attname):
    #     return f'Protocols/{self.id}/'


class Jcpaper(models.Model):
    title = models.CharField(max_length=200)
    journal = models.CharField(max_length=200)
    hwl_recommend = models.BooleanField(default=True)
    time = models.DateTimeField()
    location = models.CharField(max_length=50)
    file = models.FileField(upload_to='JC/%Y/', blank=True)
    link = models.URLField(blank=True)
    content = models.TextField()
    presenter = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('JCdetail', kwargs={'pk': self.pk})