from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('' , views.projects, name='index'),
    path('contact', views.contact, name='contact'),
    path('sensor', views.sensor, name='sensor'),
    path('sensorgraph', views.sensorgraph, name='sensorgraph'),
    path('days', views.days, name='days'),
    path('clock', views.clock, name='clock'),
    path('youtube', views.youtube, name='youtube'),
    #path('projects', views.projects, name='projects'),
    path('portal', views.portal, name='portal'),
    path('music', views.music, name='music'),
    path('movies', views.movies, name='movies'),
    path('stats', views.stats, name='stats'),
    path('wedding',views.wedding, name='wedding'),
    path('server',views.server, name='server'),
    path('resume',views.resume, name='resume')
]
