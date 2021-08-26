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
                tr = int(resp.json()['dt'])
                timefetched = (datetime.fromtimestamp(tr).strftime('%H:%M'))
                visibility = resp.json()['visibility'] / 1000
                time = datetime.now()

                context = {
                    'context':resp.json(),
                    'time':time,
                    'visibility': visibility,
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
        try:
            city = 'Sheffield'
            key = config('API_KEY')
            units = '&units=metric'
            url = 'https://api.openweathermap.org/data/2.5/weather?q='
            resp = requests.get(url + city + units + '&appid=' + key)
            tr = int(resp.json()['dt'])
            timefetched = (datetime.fromtimestamp(tr).strftime('%H:%M'))
            visibility = resp.json()['visibility'] / 1000
            time = datetime.now()

            context = {
                'context':resp.json(),
                'timefetched':timefetched,
                'time':time,
                'visibility': visibility,
                'form': CityForm
            }
        except:
            context = {
                'form': CityForm
            }
            messages.warning(request, 'No Connection to weather service')
            return render(request, 'weather/weather.html', context)


    return render(request, 'weather/weather.html', context)
