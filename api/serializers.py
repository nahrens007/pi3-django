from rest_framework import serializers
from api.models import GarageAction

class GarageActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GarageAction
        fields = ['id','created','activator']