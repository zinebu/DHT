
# Create your models here.
from django.db import models
class Dht11(models.Model):
  temp = models.FloatField(null=True)
  hum = models.FloatField(null=True)
  dt = models.DateTimeField(auto_now_add=True,null=True)
class Incident(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    operator = models.CharField(max_length=255)
    notification_app = models.CharField(max_length=255, choices=[
        ('Telegram', 'Telegram'),
        ('WhatsApp', 'WhatsApp'),
        ('Email', 'Email'),
    ])

    def __str__(self):
        return f"Incident du {self.timestamp} - {self.temperature}°C"