from django import forms
from .models import Crop

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