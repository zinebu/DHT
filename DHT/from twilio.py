from twilio.rest import Client

# Informations Twilio
account_sid = 'AC56f4f2c997ff30dc336b2605aa45c018'  # Remplacez par votre SID Twilio
auth_token = 'a939527aadff1fdc0079e294cdc8b25c'    # Remplacez par votre token d'authentification
twilio_whatsapp_number = 'whatsapp:+14155238886'  # Le numéro Twilio, à partir duquel vous enverrez les messages
receiver_whatsapp_number = 'whatsapp:+212688288202'  # Le numéro de destination (remplacez par le numéro destinataire)

# Message à envoyer
message_body = "Hello! This is a test message from Twilio."

# Initialiser le client Twilio
client = Client(account_sid, auth_token)

# Envoi du message WhatsApp
try:
    message = client.messages.create(
        from_=twilio_whatsapp_number,
        to=receiver_whatsapp_number,
        body=message_body
    )
    print(f"Message sent successfully! SID: {message.sid}")
except Exception as e:
    print(f"Failed to send message: {e}")
