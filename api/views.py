from api.models import GarageAction
from api.serializers import GarageActionSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
import RPi.GPIO as GPIO
import time

class GarageList(generics.ListCreateAPIView):
    queryset = GarageAction.objects.all()
    serializer_class = GarageActionSerializer
    def perform_create(self, serializer):
        if self.request.data.get('activator','')!="Nathan's Google Assistant":
            raise ValidationError('Invalid trigger... ' + self.request.POST.get('activator',''))
        
        # Write the "log" entry
        serializer.save()
        
        # Activate the GPIO pin controlling the relay for the garage.
        pin=18
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pin,GPIO.OUT)
        print ("GPIO Pin " +str(pin)+ " on")
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(0.5)
        print ("GPIO Pin "+str(pin)+" off")
        GPIO.output(pin,GPIO.LOW)

class GarageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GarageAction.objects.all()
    serializer_class = GarageActionSerializer

# class YoutubeList(generics.ListCreateAPIView):
#     queryset = YoutubeAction.objects.all()
#     serializer_class = YoutubeActionSerializer
#     def perform_create(self, serializer):
#         if self.request.data.get('activator','')!="Super Top Secret Activator Code":
#             raise ValidationError('Invalid trigger... ' + self.request.POST.get('activator',''))
#         else:
#             from django.conf import settings
#             import os
#             linksPath = os.path.join(settings.YT_DIR, 'links.txt')
#         serializer.save()
    