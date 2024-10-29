from django import forms
from .models import Plant, PlantType


class PlantTypeForm(forms.ModelForm):
    class Meta:
        model = PlantType
        fields = [
            'plant_type_name', 'plant_type_image',  
            'winter_irrigation_frequency', 'spring_irrigation_frequency', 
            'summer_irrigation_frequency', 'fall_irrigation_frequency'
        ]
        widgets = {
            'winter_irrigation_frequency': forms.TextInput(attrs={'placeholder': '1 - 2 Times Per Month'}),
            'spring_irrigation_frequency': forms.TextInput(attrs={'placeholder': '1 - 2 Times Per Month'}),
            'summer_irrigation_frequency': forms.TextInput(attrs={'placeholder': '1 - 2 Times Per Month'}),
            'fall_irrigation_frequency': forms.TextInput(attrs={'placeholder': '1 - 2 Times Per Month'}),
        }

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'plant_image', 'plant_type', 'sunlight_requirements', 'water_needs', 'growth_rate']

class AIRecommendationForm(forms.Form):
    soil_moisture = forms.FloatField(label="Soil Moisture Level (%)")
    sunlight_hours = forms.FloatField(label="Daily Sunlight Hours")
    rainfall_forecast = forms.FloatField(label="Rainfall Forecast (mm)")
