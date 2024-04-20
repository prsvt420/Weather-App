from datetime import datetime

import requests
from django.core.cache import cache

from WeatherApp.settings import API_KEY, ICONS_PATH


def get_weather_data(city):
    weather_data = cache.get(f'weather_data-{city}')

    if not weather_data:
        weather_data = {}

        url = f'http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&aqi=no'
        response_data = requests.get(url).json()

        weather_data['CITY'] = response_data['location']['name']

        localtime = response_data['location']['localtime']

        weather_data['DATE'] = {
            'DAY': localtime.split()[0].split('-')[2],
            'MONTH': datetime.strptime(localtime, '%Y-%m-%d %H:%M').strftime('%B'),
            'YEAR': localtime.split()[0].split('-')[0]
        }

        weather_data['DAY_OF_WEEK'] = datetime.strptime(localtime, '%Y-%m-%d %H:%M').strftime('%A')
        weather_data['TEMPERATURE'] = response_data['current']['temp_c']
        weather_data['CONDITION'] = response_data['current']['condition']['text']
        weather_data['ICON_PATH'] = ICONS_PATH + response_data['current']['condition']['icon'].split('/', 5)[-1]
        weather_data['PRECIPITATION'] = int(response_data['current']['precip_mm'])
        weather_data['HUMIDITY'] = response_data['current']['humidity']
        weather_data['WIND_SPEED'] = int(response_data['current']['wind_kph'])
        weather_data['FORECAST'] = get_forecast_weather_data(city)

        cache.set(f'weather_data-{city}', weather_data, 60)

    return weather_data


def get_forecast_weather_data(city):
    url = f'http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=5&aqi=no&alerts=no'
    response_data = requests.get(url).json()

    forecast_weather_data = []

    for day in response_data['forecast']['forecastday'][1:]:
        date = day['date']

        forecast_weather_data.append({
            'DAY_OF_WEEK': datetime.strptime(date, '%Y-%m-%d').strftime('%A')[0:3],
            'TEMPERATURE': day['day']['maxtemp_c'],
            'ICON_PATH': ICONS_PATH + day['day']['condition']['icon'].split('/', 5)[-1]
        })

    return forecast_weather_data
