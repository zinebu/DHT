from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
import requests
from .models import Incident
from .serializers import IncidentSerializer
from django.shortcuts import render

# Fonction pour envoyer des messages Telegram
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.status_code, response.text

@api_view(["GET", "POST"])
def Dlist(request):
    if request.method == "GET":
        # Récupérer toutes les données du modèle Dht11
        all_data = Dht11.objects.all()
        data_ser = DHT11serialize(all_data, many=True)  # Sérialisation en JSON
        return Response(data_ser.data)

    elif request.method == "POST":
        # Sérialiser les données reçues
        serial = DHT11serialize(data=request.data)

        if serial.is_valid():
            # Sauvegarder les données dans la base de données
            serial.save()

            # Récupérer la dernière température
            derniere_temperature = Dht11.objects.last().temp
            print(f"Dernière température enregistrée : {derniere_temperature}")

            # Vérifier si la température dépasse le seuil de 15°C
            if derniere_temperature > 25:
                alert_message = (
                    "La température dépasse le seuil de 25°C, veuillez intervenir immédiatement "
                    "pour vérifier et corriger cette situation."
                )

                # Envoyer une alerte par email
                subject = 'Alerte de température élevée'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['salma.ayache.23@ump.ac.ma']
                send_mail(subject, alert_message, email_from, recipient_list)

                # Envoyer une alerte via WhatsApp
                account_sid = 'AC56f4f2c997ff30dc336b2605aa45c018'
                auth_token = 'a939527aadff1fdc0079e294cdc8b25c'
                client = Client(account_sid, auth_token)
                client.messages.create(
                    from_='whatsapp:+14155238886',
                    body=alert_message,
                    to='whatsapp:+212688288202'
                )

                # Envoyer une alerte via Telegram
                telegram_token = '8176663468:AAFC3pFlAf3S3TJWMlniJc2uyyJmqbEBMpU'  # Remplacez par votre token Telegram
                chat_id = '6965485537'  # Remplacez par votre ID de chat
                status_code, response_text = send_telegram_message(telegram_token, chat_id, alert_message)
                print(f"Code de réponse Telegram : {status_code}")
                print(f"Réponse Telegram : {response_text}")

                # Vérifier si le message a été envoyé avec succès
                if status_code == 200:
                    print("Le message a été envoyé avec succès à Telegram.")
                else:
                    print("Erreur lors de l'envoi du message à Telegram.")

            return Response(serial.data, status=status.HTTP_201_CREATED)
        else:
            # Retourner les erreurs de validation
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def incidents_view(request):
    incidents = Incident.objects.all().order_by('-timestamp')  # Trie les incidents par date (du plus récent au plus ancien)
    return render(request, 'incidents.html', {'incidents': incidents})

