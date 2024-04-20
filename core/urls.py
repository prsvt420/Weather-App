from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('weather/', views.WeatherPageView.as_view(), name='index'),
]
