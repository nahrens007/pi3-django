from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('sensor', views.sensor, name='sensor'),
    path('sensorgraph', views.sensorgraph, name='sensorgraph'),
    path('days', views.days, name='days'),
    path('clock', views.clock, name='clock'),
    path('clocksettings', views.clocksettings, name='clocksettings'),
    path('projects', views.projects, name='projects'),
    path('portal', views.portal, name='portal'),
]
