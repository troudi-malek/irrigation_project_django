# forms.py
from django import forms
from .models import WeatherData,IrrigationPlan


class WeatherDataForm(forms.ModelForm):
    class Meta:
        model = WeatherData
        fields = ['city', 'temperature', 'humidity', 'precipitation', 'irrigation_need',]  # Adjust fields as needed
        
        
class IrrigationPlanForm(forms.ModelForm):
    class Meta:
        model = IrrigationPlan
        fields = ['weather_data', 'frequency', 'start_time', 'duration']