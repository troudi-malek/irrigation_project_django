import requests
from dotenv import load_dotenv
import os

load_dotenv()


def get_weather_data(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
        
def calculate_irrigation_needs(weather_data):
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    precipitation = weather_data.get('rain', {}).get('1h', 0)

    if precipitation > 0:
        water_needed = max(0, 10 - precipitation)  
    else:
        water_needed = 10 + (temperature - 20) * 0.5  

    return max(0, water_needed)  # Ensure water needed is non-negative

