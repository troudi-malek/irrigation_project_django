# data_processing.py
import pandas as pd
from .models import WeatherData

def get_weather_data_for_clustering():
    # Fetch data from WeatherData model
    weather_data = WeatherData.objects.all()
    data = pd.DataFrame.from_records(
        weather_data.values("city", "temperature", "humidity", "precipitation", "irrigation_need")
    )
    
    # Group by city to get average values per city
    data = data.groupby("city").mean().reset_index()
    
    return data
