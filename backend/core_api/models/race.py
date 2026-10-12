from django.db import models

# Create your models here.
class Race(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=100, blank=True, default="")
    dateRan=models.DateTimeField()

class Result(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=100, blank=True, default="")
    found = models.BooleanField(default=False)