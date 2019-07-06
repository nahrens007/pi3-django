from django.contrib import admin

# Import models to be registered
from .models import Days, Movie, Contact

# Register your models here.
admin.site.register(Days)
admin.site.register(Movie)
admin.site.register(Contact)