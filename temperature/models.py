from django.db import models

# Create your models here.
class Visitor(models.Model):
    visit_date = models.DateTimeField(auto_now=True)
    def get_date(self):
        return self.visit_date

class Contact(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    subject = models.CharField(max_length=256)
    contact_date = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=1024)
    
class Days(models.Model):
    startYear = models.CharField("start year", max_length=4, default="N")
    startMonth = models.CharField("start month", max_length=2, default="N")
    startDate = models.CharField("start date", max_length=2, default="N")
    endYear = models.CharField("end year", max_length=4, default="N")
    endMonth = models.CharField("end month", max_length=2, default="N")
    endDate = models.CharField("end date", max_length=2, default="N")
    description = models.CharField("description", max_length=255, default="")
    
    class Meta:
        unique_together=('startYear', 'startMonth', 'startDate', 'endYear', 'endMonth', 'endDate')
        
class Movie(models.Model):
    title = models.CharField("title", max_length=128, default="")
    info = models.CharField("info", max_length=128, default="")