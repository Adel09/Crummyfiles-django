
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class File(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=10)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=400, blank=True)
    file = models.FileField(upload_to='uploads/')
    date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


#Not used but don't remove for now
class Link(models.Model):
    uuid = models.CharField(max_length=10)
    file = models.ForeignKey('File', on_delete=models.CASCADE)

class Clipboard(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=10)
    content = models.CharField(max_length=2500, default="")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

