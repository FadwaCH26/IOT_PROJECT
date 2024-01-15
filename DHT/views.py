from django.shortcuts import render
from .models import Dht11  # Assurez-vous d'importer le modèle Dht11
from django.utils import timezone
import csv
from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime,timedelta
import telepot
from twilio.rest import Client
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticating the user
        user = authenticate(request, username=username, password=password)
        # Checking if authentication is successful
        if user is not None:
            login(request, user)
            return render(request,'home.html')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')

@login_required()
def index(request):
    return render(request,'home.html')
@login_required()
def tempbyday(request):
    return render(request,'TempByDay.html')
@login_required()
def tempbyweek(request):
    return render(request,'TempByWeek.html')
@login_required()
def tempbymonth(request):
    return render(request,'TempByMonth.html')
@login_required()
def humbyday(request):
    return render(request,'HumByDay.html')
@login_required()
def humbyweek(request):
    return render(request,'HumByWeek.html')
@login_required()
def humbymonth(request):
    return render(request,'HumByMonth.html')
@login_required()
def showdata(request):
    dht_data = Dht11.objects.all()
    return render(request , 'data_table.html',{'dht_data': dht_data})
@login_required()
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

@login_required()
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
@login_required()
def index_view(request):
    return render(request, 'index.html')

@login_required
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
@login_required
def index_view(request):
    return render(request, 'index.html')
#pour afficher les graphes
@login_required
def graphique(request):
    return render(request, 'Chart.html')
# récupérer toutes les valeur de température et humidity sous forme un #fichier json
@login_required
def chart_data(request):
    dht = Dht11.objects.all()

    data = {
        'temps': [datetime.strftime(Dt.dt, "%m") for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier 24h
# et envoie sous forme JSON
@login_required
def chart_data_jour(request):
    dht = Dht11.objects.all()
    now = timezone.now()

    # Récupérer l'heure il y a 24 heures
    last_24_hours = now - timezone.timedelta(hours=24)

    # Récupérer tous les objets de Module créés au cours des 24 dernières heures
    dht = Dht11.objects.filter(dt__range=(last_24_hours, now))
    data = {
        'temps': [datetime.strftime(Dt.dt, "%m") for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier semaine
# et envoie sous forme JSON
@login_required
def chart_data_semaine(request):
    dht = Dht11.objects.all()
    # Calculate the start date of the previous week
    date_debut_semaine = timezone.now().date() - timedelta(days=7)
    print(timedelta(days=7))
    print(date_debut_semaine)

    # Filter records created since the start of the previous week
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)

    data = {
        'temps': [datetime.strftime(Dt.dt, "%m") for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }

    return JsonResponse(data)

#pour récupérer les valeurs de température et humidité de dernier moins
# et envoie sous forme JSON
@login_required
def chart_data_mois(request):

    date_debut_semaine = timezone.now().date() - timedelta(days=30)
    print(timedelta(days=30))
    print(date_debut_semaine)

    # filtrer les enregistrements créés depuis le début de la semaine dernière
    dht = Dht11.objects.filter(dt__gte=date_debut_semaine)

    data = {
        'temps': [datetime.strftime(Dt.dt, "%m") for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht]
    }
    return JsonResponse(data)

def sendtele(dht):
    token = '6351788178:AAFB8Lpt_DzFzJ2SSNKKlvWjmCaLJvhiDro'
    rece_id = 2141917333
    bot = telepot.Bot(token)
    message = f'🚨 Urgent Alert: Temperature Abnormality Detected! 🚨\n\n'
    message += f'🌡️ Current Temperature: {dht.temp}°C 💧 Humidity: {dht.hum}% ⏰ Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

    bot.sendMessage(rece_id, message)
def sendwhatsap():
    account_sid = 'AC0fb72eac5ca7aba4fa821b4186fad348'
    auth_token = 'e4d016ef5eb781b45450e2e224b4d07d'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=f'🚨 Urgent Alert: Temperature Abnormality Detected! 🚨\n',
        to='whatsapp:+212762491085'
    )

