from django.urls import path
from .views import fetch_weather
from .views import weather_list
from .views import delete_weather
from .views import update_weather
from .views import client_weather_list
from .views import irrigationNeed
from .views import city_clustering_view

from . import views


urlpatterns = [
    
        path('climate/', fetch_weather, name='fetch_weather'),
        path('weather/', weather_list, name='weather_list'),
        path('weather/delete/<int:id>/', delete_weather, name='delete_weather'),
        path('weather/update/<int:id>/', update_weather, name='update_weather'),
        
        
        
     path('irrigation-plans/', views.irrigation_plan_list, name='irrigation_plan_list'),
     path('irrigation-plans/create/', views.add_irrigation_plan, name='add_irrigation_plan'),
     path('irrigation-plans/<int:id>/update/', views.update_irrigation_plan, name='update_irrigation_plan'),
     path('irrigation-plans/<int:id>/delete/', views.delete_irrigation_plan, name='delete_irrigation_plan'),
     
     
    path('clientWeather/', client_weather_list, name='client_weather_list'),
    path('clientWeather/irrigationNeed/', irrigationNeed, name='irrigationNeed'), 
    
    
    
        path('climate_clusters/', views.city_clustering_view, name='climate_clusters'),
]







