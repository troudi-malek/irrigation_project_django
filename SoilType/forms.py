from django import forms
from .models import Land, SoilType


class LandForm(forms.ModelForm):
    class Meta:
        model = Land
        fields = ['location', 'area_size', 'soil_type']
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter land location'}),
            'area_size': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter area size'}),
            'soil_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select soil type'}),
        }


class SoilTypeForm(forms.ModelForm):
    class Meta:
        model = SoilType
        fields = ['type_name', 'water_retention_capacity', 'permeability_rate']
        widgets = {
            'type_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter soil type name'}),
            'water_retention_capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Water retention capacity (%)'}),
            'permeability_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Permeability rate'}),
        }
        labels = {
            'type_name': 'Soil Type Name',
            'water_retention_capacity': 'Water Retention Capacity (%)',
            'permeability_rate': 'Permeability Rate',
        }
