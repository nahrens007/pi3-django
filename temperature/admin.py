from django.contrib import admin

# Import models to be registered
from .models import Days

# Register your models here.
admin.site.register(Days)
