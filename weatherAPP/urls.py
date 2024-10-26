from django.urls import path
from .views import fetch_weather
from .views import weather_list
from .views import delete_weather
from .views import update_weather

urlpatterns = [
    
        path('climate/', fetch_weather, name='fetch_weather'),
        path('weather/', weather_list, name='weather_list'),
        path('weather/delete/<int:id>/', delete_weather, name='delete_weather'),
        path('weather/update/<int:id>/', update_weather, name='update_weather'),






]