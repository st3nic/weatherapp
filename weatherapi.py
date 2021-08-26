import requests
from datetime import datetime, timedelta


key = '468161cd0d25281e214a1c9146a5bcb7'

units = '&units=metric'

url = 'https://api.openweathermap.org/data/2.5/weather?q='

resp = requests.get(url + 'Birmingham,gb' + '&appid=' + key )


print(resp.json())
