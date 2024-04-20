from django.shortcuts import render
from django.views import View

from core.utils import get_weather_data


class WeatherPageView(View):
    @staticmethod
    def get(request):
        city = request.GET.get('city')
        context = get_weather_data(city)
        return render(request, 'core/weather_page.html', context)
