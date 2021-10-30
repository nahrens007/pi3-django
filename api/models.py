from django.db import models

# Create your models here.
class GarageAction(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    activator = models.CharField(max_length=100, blank=True, default='')