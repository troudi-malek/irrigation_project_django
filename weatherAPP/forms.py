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
    
    def __init__(self, *args, **kwargs):
        super(IrrigationPlanForm, self).__init__(*args, **kwargs)
        # Ensure the weather_data field is a dropdown (list) of WeatherData instances
        self.fields['weather_data'].queryset = WeatherData.objects.all()