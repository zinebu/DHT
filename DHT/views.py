from django.shortcuts import render
from .models import Dht11  # Assurez-vous d'importer le modèle Dht11
from django.utils import timezone
import csv
from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from .models import Incident
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SuperUserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging
import json

def incidents_to_json(request):
    # Récupérer tous les incidents de la base de données
    incidents = Incident.objects.all()

    # Convertir les incidents en une liste de dictionnaires
    incidents_data = list(incidents.values('timestamp', 'temperature', 'operator', 'notification_app'))

    # Retourner la réponse en format JSON
    return JsonResponse(incidents_data, safe=False)
def home(request):
    return render(request, 'home.html')

def table(request):
    derniere_ligne = Dht11.objects.last()
    derniere_date = Dht11.objects.last().dt
    delta_temps = timezone.now() - derniere_date
    difference_minutes = delta_temps.seconds // 60
    temps_ecoule = ' il y a ' + str(difference_minutes) + ' min'
    if difference_minutes > 60:
        temps_ecoule = 'il y ' + str(difference_minutes // 60) + 'h' + str(difference_minutes % 60) + 'min'
    valeurs = {'date': temps_ecoule, 'id': derniere_ligne.id, 'temp': derniere_ligne.temp, 'hum': derniere_ligne.hum}
    return render(request, 'value.html', {'valeurs': valeurs})

def download_csv(request):
    model_values = Dht11.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dht.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response
#pour afficher navbar de template
def index_view(request):
    return render(request, 'index.html')

#pour afficher les graphes
def graphiqueTemp(request):
    return render(request, 'ChartTemp.html')
# récupérer toutes les valeur de température et humidity sous forme un #fichier json
def graphiqueHum(request):
    return render(request, 'ChartHum.html')
# récupérer toutes les valeur de température et humidity sous forme un #fichier json
def chart_data(request):
    dht = Dht11.objects.all()

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)
def chart_data(request):
    dht = Dht11.objects.all()

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier 24h
# et envoie sous forme JSON
def chart_data_jour(request):
    dht = Dht11.objects.all()
    now = timezone.now()

    # Récupérer l'heure il y a 24 heures
    last_24_hours = now - timezone.timedelta(hours=24)

    # Récupérer tous les objets de Module créés au cours des 24 dernières heures
    dht = Dht11.objects.filter(dt__range=(last_24_hours, now))
    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier semaine
# et envoie sous forme JSON
def chart_data_semaine(request):
    dht = Dht11.objects.all()
    # calcul de la date de début de la semaine dernière
    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=7)
    print(datetime.timedelta(days=7))
    print(date_debut_semaine)

    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }

    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier moins
# et envoie sous forme JSON
def chart_data_mois(request):
    dht = Dht11.objects.all()

    date_debut_semaine = timezone.now().date() - datetime.timedelta(days=30)
    print(datetime.timedelta(days=30))
    print(date_debut_semaine)

    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)

    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def sendtele():
    token = '6662023260:AAG4z48OO9gL8A6szdxg0SOma5hv9gIII1E'
    rece_id = 1242839034
    bot = telepot.Bot(token)
    bot.sendMessage(rece_id, 'la température depasse la normale')
    print(bot.sendMessage(rece_id, 'OK.'))

def incidents_view(request):
    incidents = Incident.objects.order_by('-timestamp')[:10]  # Récupérer les 10 derniers incidents
    return render(request, 'incidents.html', {'incidents': incidents})

@login_required
def create_superuser(request):
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour accéder à cette page.")
        return redirect('home')  # Rediriger vers une autre page appropriée

    if request.method == 'POST':
        form = SuperUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Créer un super-utilisateur
            User.objects.create_superuser(username=username, email=email, password=password)
            messages.success(request, f"Super-utilisateur {username} créé avec succès.")
            return redirect('create_superuser')
    else:
        form = SuperUserCreationForm()

    return render(request, 'create_superuser.html', {'form': form})


@login_required
def manage_admins(request):
    if not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas les permissions nécessaires pour accéder à cette page.")
        return redirect('home')

    admins = User.objects.filter(is_superuser=True)

    if request.method == 'POST':
        action = request.POST.get('action')
        admin_id = request.POST.get('admin_id')

        if action == 'delete':
            admin = get_object_or_404(User, id=admin_id, is_superuser=True)
            if admin == request.user:
                messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
            else:
                admin.delete()
                messages.success(request, f"Le compte administrateur {admin.username} a été supprimé avec succès.")
        elif action == 'reset_password':
            admin = get_object_or_404(User, id=admin_id, is_superuser=True)
            new_password = request.POST.get('new_password')
            if new_password:
                admin.set_password(new_password)
                admin.save()
                messages.success(request, f"Le mot de passe de {admin.username} a été réinitialisé avec succès.")

    return render(request, 'manage_admins.html', {'admins': admins})


@login_required
def gestion_utilisateurs(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirige les utilisateurs non super-admins

    # Liste des administrateurs
    admins = User.objects.filter(is_superuser=True)

    # Formulaire pour créer un nouvel administrateur
    if request.method == "POST":
        if 'create_admin' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Un administrateur avec ce nom d'utilisateur existe déjà.")
            else:
                User.objects.create_superuser(username=username, email=email, password=password)
                messages.success(request, "Super-utilisateur créé avec succès.")
                return redirect('gestion_utilisateurs')  # Rediriger après création

        elif 'delete_admin' in request.POST:
            admin_id = request.POST.get('admin_id')
            try:
                admin = User.objects.get(id=admin_id, is_superuser=True)
                admin.delete()
                messages.success(request, "Super-utilisateur supprimé avec succès.")
            except User.DoesNotExist:
                messages.error(request, "Administrateur introuvable.")

        elif 'reset_password' in request.POST:
            admin_id = request.POST.get('admin_id')
            new_password = request.POST.get('new_password')
            try:
                admin = User.objects.get(id=admin_id, is_superuser=True)
                admin.set_password(new_password)
                admin.save()
                messages.success(request, "Mot de passe mis à jour avec succès.")
            except User.DoesNotExist:
                messages.error(request, "Administrateur introuvable.")

    return render(request, 'gestion_utilisateurs.html', {'admins': admins})
def logout_view(request):
    logout(request)
    return redirect('authen') 

from django.contrib.auth import authenticate, login, logout

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info(f"User {username} logged in.")
            return redirect('table')
        else:
            logger.info(f"Failed login attempt for {username}.")
    return render(request, 'authen.html')

def logout_view(request):
    logout(request)
    request.session.flush()
    logger.info("User logged out and session flushed.")
    return redirect('authen')

from django.http import JsonResponse
from datetime import datetime, timedelta

# Exemple de fonction pour obtenir les données de température pour aujourd'hui
def get_temperature_data_aujourdhui(request):
    # Exemple de données générées aléatoirement
    labels = []
    tempData = []
    current_time = datetime.now()

    for i in range(10):
        labels.append(current_time.strftime('%Y-%m-%d %H:%M'))
        tempData.append(round(14 + (random.random() * 4 - 2), 2))  # Température entre 12°C et 16°C
        current_time -= timedelta(hours=1)  # Décaler d'une heure

    return JsonResponse({'labels': labels, 'tempData': tempData})

# Exemple de fonction pour obtenir les données de température pour la semaine
def get_temperature_data_semaine(request):
    labels = []
    tempData = []
    current_time = datetime.now()

    for i in range(7):
        labels.append((current_time - timedelta(days=i)).strftime('%Y-%m-%d'))
        tempData.append(round(14 + (random.random() * 4 - 2), 2))  # Température entre 12°C et 16°C

    return JsonResponse({'labels': labels, 'tempData': tempData})

# Exemple de fonction pour obtenir les données de température pour le mois
def get_temperature_data_mois(request):
    labels = []
    tempData = []
    current_time = datetime.now()

    for i in range(30):
        labels.append((current_time - timedelta(days=i)).strftime('%Y-%m-%d'))
        tempData.append(round(14 + (random.random() * 4 - 2), 2))  # Température entre 12°C et 16°C

    return JsonResponse({'labels': labels, 'tempData': tempData})



