from django.db import models
from django.utils import timezone

class City(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name}"
