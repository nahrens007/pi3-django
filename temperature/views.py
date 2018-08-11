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
    return render(request, 'index.html', context)

def contact(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        contact = models.Contact(first_name=first_name, last_name=last_name, email=email, subject=subject, message=message)
        contact.save()
        
        msg = 'First Name: ' + first_name + '\nLast Name: ' + last_name + '\nSubject: ' + subject + '\nEmail: ' + email + '\nMessage: \n' + message
        
        from django.core.mail import send_mail
        send_mail('Contact Website', msg, 'contact@nathanahrens.com', ['contact@nathanahrens.com'],fail_silently=True)
        
        context = {
            'subject':subject,
            'name':first_name + " " + last_name,
            'email':email,
            'message':message,
        }
        return render(request, 'email_contact.html', context)
        
    # default form
    context = {
    }
    return render(request, 'contact.html', context)

def sensor(request):
    if 'min' in request.GET:
        try:
            minutes = int(request.GET['min'])
        except ValueError:
            return render(request, 'sensor.html', {'error_message':'You must enter an integer.'})
        
        from django.db import connection
        cursor = connection.cursor()
        if minutes == 0: 
            cursor.execute("SELECT * FROM sensor_readings;")
            context = {
                'rowcount': cursor.rowcount,
            }
            return render(request, 'sensor.html', context)
        else:
            cursor.execute("SELECT * FROM sensor_readings WHERE date > NOW() - INTERVAL %s MINUTE;", [minutes])
            results = cursor.fetchall()
            context = {
                'results': results,
            }
            return render(request, 'sensor.html', context)
        
    return render(request, 'sensor.html', {})

def sensorgraph(request):
    context = {

    }
    return render(request, 'sensorgraph.html', context)

def days(request):
    import datetime
    
    now = datetime.date.today()
    rows = models.Days.objects.all()
    dates = []
    for row in rows:
        date = {}
        startYear = row.startYear if row.startYear != 'N' else now.strftime("%Y")
        startMonth = row.startMonth if row.startMonth!='N' else now.strftime("%m")
        startDate = row.startDate if row.startDate!='N' else now.strftime("%d")
        
        endYear = row.endYear if row.endYear!='N' else now.strftime("%Y")
        endMonth = row.endMonth if row.endMonth!='N' else now.strftime("%m")
        endDate = row.endDate if row.endDate!='N' else now.strftime("%d")
        
        start = datetime.datetime.strptime(str(startYear)+"/"+str(startMonth)+"/"+str(startDate), "%Y/%m/%d").date()
        end = datetime.datetime.strptime(str(endYear)+"/"+str(endMonth)+"/"+str(endDate), "%Y/%m/%d").date()
        
        if start > end:
            date['start']=end
            date['end']=start
        else:
            date['start']=start
            date['end']=end
        
        date['days']=(end-start).days
        
        dates.append(date)
        
    context = {
        'dates':dates
    }
    return render(request, 'days.html', context)

def clock(request):
    context = {
    }
    return render(request, 'clock.html', context)

def clocksettings(request):
    context = {
        'count': '5',
        'file':'File Contents',
    }
    return render(request, 'clock_settings.html', context)

def projects(request):
    context = {}
    return render(request, 'projects.html', context)
    
def portal(request):
    from temperature.urls import urlpatterns
    urls = []
    for url in urlpatterns:
        urls.append(url)
    context = {'urls':urls}
    return render(request, 'portal.html', context)