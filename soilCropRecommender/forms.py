from django import forms
from .models import Crop,Field,Prediction

class CropForm(forms.ModelForm):
    class Meta:
        model=Crop
        fields=['name','water_need','growth_stage','optimal_temperature']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter crop name'}),
            'water_need': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Water need'}),
            'growth_stage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter growth stage'}),
            'optimal_temperature': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Optimal temperature'}),
        }

class FieldForm(forms.ModelForm):
    class Meta:
        model=Field
        fields=['location','area_size','soil_quality','crop']
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Field Location'}),
            'area_size': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter area size'}),
            'soil_quality': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select soil quality'}),
            'crop':forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select crop'})
        }

class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['REGION', 'TEMPERATURE', 'WEATHER_CONDITION']

        # Optional: You can add widgets or customize labels
        widgets = {
            'TEMPERATURE': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter temperature'}),
            'REGION': forms.Select(attrs={'class': 'form-control'}),
            'WEATHER_CONDITION': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'REGION': 'Region Type',
            'TEMPERATURE': 'Temperature (°C)',
            'WEATHER_CONDITION': 'Weather Condition',
        }

