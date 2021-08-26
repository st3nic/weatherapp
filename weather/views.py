from django.shortcuts import render
from decouple import config
import requests
from datetime import datetime
from .forms import CityForm
from django.contrib import messages
from pytz import timezone



def weather(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CityForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            try:
                city = request.POST.get('city')
                key = config('API_KEY')
                units = '&units=metric'
                url = 'https://api.openweathermap.org/data/2.5/weather?q='
                resp = requests.get(url + city + '&appid=' + key + units)
                sr = int(resp.json()['sys']['sunrise'])
                sunrise = (datetime.utcfromtimestamp(sr).strftime('%H:%M'))
                ss = int(resp.json()['sys']['sunset'])
                sunset = (datetime.utcfromtimestamp(ss).strftime('%H:%M'))
                time = datetime.now()

                context = {
                    'context':resp.json(),
                    'sunrise':sunrise,
                    'sunset':sunset,
                    'time':time,
                    'form': CityForm
                }
            except:
                if resp.status_code != 200:
                    context = {
                    'form': CityForm
                    }
                    messages.warning(request, 'Please enter a valid city!') 
                    return render(request, 'weather/weather.html', context)



    else:
        city = 'Sheffield'
        key = config('API_KEY')
        units = '&units=metric'
        url = 'https://api.openweathermap.org/data/2.5/weather?q='
        resp = requests.get(url + city + units + '&appid=' + key)
        sr = int(resp.json()['sys']['sunrise'])
        sunrise = (datetime.utcfromtimestamp(sr).strftime('%H:%M'))
        ss = int(resp.json()['sys']['sunset'])
        sunset = (datetime.utcfromtimestamp(ss).strftime('%H:%M'))
        time = datetime.now()

        context = {
            'context':resp.json(),
            'sunrise':sunrise,
            'sunset':sunset,
            'time':time,
            'form': CityForm
        }

    return render(request, 'weather/weather.html', context)
