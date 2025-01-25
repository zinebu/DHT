#from rest_framework import serializers
#from .models import Dht11
#class DHT11serialize(serializers.ModelSerializer):
 #class Meta :
        #  model = Dht11
         # fields = ['temp', 'hum'] 

from rest_framework import serializers
from .models import Dht11, Incident

# Sérialiseur pour le modèle Dht11
class DHT11serialize(serializers.ModelSerializer):
    temperature = serializers.FloatField(source='temp')
    humidity = serializers.FloatField(source='hum')

    class Meta:
        model = Dht11
        fields = ['temperature', 'humidity']

# Sérialiseur pour le modèle Incident
class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ['timestamp', 'temperature', 'operator', 'notification_app']
