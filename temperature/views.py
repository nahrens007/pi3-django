from django.shortcuts import render
from . import models
from django.contrib.auth.decorators import login_required
import requests
import json

requests.packages.urllib3.disable_warnings()

# Create your views here.
def index(request):

    # Create new visitor entry in table
    #visitor = models.Visitor()
    #visitor.save()

    # Get the total count of visitors in table
    #count = str(models.Visitor.objects.all().count())

    context = {}
    return render(request, 'index.html', context)

def resume(request):
    return render(request, 'resume.html', {})

def contact(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        fail_cont = {
            'error_message':'You must complete the reCAPTCHA.',
            'subject':subject,
            'first_name':first_name,
            'last_name':last_name,
            'email':email,
            'message':message
        }
        # Google Recaptcha code
        resp = verify_recap(request.POST['g-recaptcha-response'])
        if resp.status_code==200 and resp.text:
            res = json.loads(resp.text)
            if res['success'] != True or res['hostname'] != 'www.nathanahrens.com':
                return render(request, 'contact.html', fail_cont)
        else:
            return render(request, 'contact.html', fail_cont)
        
        contact = models.Contact(first_name=first_name, last_name=last_name, email=email, subject=subject, message=message)
        contact.save()
        
        msg = 'First Name: ' + first_name + '\nLast Name: ' + last_name + '\nSubject: ' + subject + '\nEmail: ' + email + '\nMessage: \n' + message
        
        from django.core.mail import send_mail
        send_mail('nathanahrens.com', msg, 'contact@nathanahrens.com', ['contact@nathanahrens.com'],fail_silently=True)
        
        context = {
            'subject':subject,
            'name':first_name + " " + last_name,
            'email':email,
            'message':message,
        }
        return render(request, 'email_contact.html', context)
        
    # default form
    return render(request, 'contact.html', {})

def sensor(request):
    if 'min' in request.GET:
        try:
            minutes = int(request.GET['min'])
        except ValueError:
            return render(request, 'sensor.html', {'error_message':'You must enter an integer.'})
        
        from django.db import connection
        cursor = connection.cursor()
        if minutes == 0: 
            cursor.execute("SELECT COUNT(*) FROM sensor_readings;")
            context = {
                'rowcount': cursor.fetchall(),
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

def stats(request):
    from django.db import connection
    cursor = connection.cursor()
    # Select most recent row
    #  select * from sensor_readings order by date desc limit 1;
    cursor.execute("SELECT * FROM sensor_readings ORDER BY date DESC LIMIT 1;")
    results = cursor.fetchall()
    
    return render(request, 'stats.html', {'results':results})
    
def server(request):
    import os
    hostname='warehouse'
    if request.method == 'POST':
        if 'wake' in request.POST:
            #send WOL /usr/bin/wakeonlan 90:2b:34:5c:78:78
            os.system('/usr/bin/wakeonlan 90:2b:34:5c:78:78')
        if 'shutdown' in request.POST:
            os.system('/usr/bin/curl -v http://warehouse/command/shutdown')
        if 'restart' in request.POST:
            os.system('/usr/bin/curl -v http://warehouse/command/restart')
    response = os.system("ping -c 1 -w2 " + hostname + " > /dev/null 2>&1")
    status=True if response == 0 else False
    return render(request, 'server.html', {'status':status})
    
def sensorgraph(request):
    context = {

    }
    return render(request, 'sensorgraph.html', context)

def clock(request):
    context = {
    }
    return render(request, 'clock.html', context)

def wedding(request):
    context = {
    }
    return render(request, 'wedding.html', context)

@login_required
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
        
        date['description'] = row.description
        
        dates.append(date)
        
    context = {
        'dates':dates
    }
    return render(request, 'days.html', context)
    
@login_required
def youtube(request):
    from django.conf import settings
    import os
    
    linksPath = os.path.join(settings.YT_DIR, 'links.txt')
    
    # Need to write the contents of POST to the file.
    if request.method == 'POST':
        links = open(linksPath, 'w')
        contents = request.POST['links']
        links.write(contents)
        links.close()
    
    # Read the contents of the file and display.
    links = open(linksPath, 'r')
    contents = links.read()
    links.close()
    context = {
        'file':contents,
    }
    return render(request, 'youtube.html', context)

def projects(request):
    context = {}
    return render(request, 'projects.html', context)

@login_required    
def portal(request):
    from temperature.urls import urlpatterns
    urls = []
    for url in urlpatterns:
        urls.append(url)
    context = {'urls':urls}
    return render(request, 'portal.html', context)

@login_required
def music(request):
    from django.conf import settings
    import json
    import os
    
    linksPath = os.path.join(settings.YT_DIR, 'links.txt')
    nextId = 0
    try:
        linksF = open(linksPath, 'r')
        songs = json.loads(linksF.read())
        linksF.close()
    except:
        songs = []
    

    data=''
    if request.method == 'POST':
        if 'remove' in request.POST:
            for i in range(len(songs)):
                if songs[i]['id'] == int(request.POST['remove']):
                    del songs[i]
        else:
            url = request.POST.get('url', '')
            title = request.POST.get('title', '')
            artist = request.POST.get('artist', '')
            album = request.POST.get('album', '')
            for song in songs:
                if 'id' in song:
                    nextId = song['id'] + 1
            songs.append({'id':nextId, 'url':url, 'title':title, 'artist':artist, 'album':album})
            
        f = open(linksPath, 'w')
        f.write(json.dumps(songs))
        f.close()
        

    context = {
        'songs':songs
    }
     
    return render(request, 'music.html', context)

@login_required
def movies(request):
    rows = models.Movie.objects.all()
    
    if request.method == 'POST':
        if 'submit' in request.POST:
            if request.POST['submit'] == 'Add':
                movie = models.Movie(title=request.POST.get('title', ''), info=request.POST.get('info', ''))
                movie.save()
            elif request.POST['submit'] == 'Edit':
                pass
    # movies = []
    # for row in rows:
    #     movie = {}
    #     movie['title'] = row.title
    #     movie['info'] = row.info
        
    #     movies.append(movie)
        
    context = {
        'movies':rows
    }
    return render(request, 'movies.html', context)

def verify_recap(code):
    session = requests.session()
    return session.post('https://www.google.com/recaptcha/api/siteverify',
                data={'secret':'6Lf8RLUUAAAAADgAjL7kJQOD3WvwQvfTsmBTFYMD','response':code},
                verify=False)
