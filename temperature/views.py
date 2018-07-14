from django.shortcuts import render
from . import models

# Create your views here.
def index(request):

    # Create new visitor entry in table
    visitor = models.Visitor()
    visitor.save()

    # Get the total count of visitors in table
    count = str(models.Visitor.objects.all().count())

    context = {
        'visit_count': count,
    }
    return render(request, 'temperature/index.html', context)

def contact(request):
    context = {

    }
    return render(request, 'temperature/contact.html', context)

def sensor(request):
    context = {

    }
    return render(request, 'temperature/sensor.html', context)

def sensorgraph(request):
    context = {

    }
    return render(request, 'temperature/sensorgraph.html', context)

def days(request):
    import datetime
    current = datetime.date.today()
    begin = datetime.date(2017, 8, 22)
    days = (current - begin).days
    context = {
        'days': str(days),
        'begin': begin.strftime("%m-%d-%Y"),
        'current': current.strftime("%m-%d-%Y"),

    }
    return render(request, 'temperature/days.html', context)

def clock(request):
    context = {
        'count': '5',
        'file':'File Contents',
    }
    return render(request, 'temperature/clock.html', context)

