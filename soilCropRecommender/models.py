from django.db import models

class Crop(models.Model):
    name=models.CharField(max_length=30)
    water_need=models.DecimalField(max_digits=5,decimal_places=2)
    growth_stage = models.CharField(max_length=50)
    optimal_temperature = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Field(models.Model):
    SOIL_TYPES = [
        ('DRY', 'DRY'),
        ('HUMID', 'HUMID'),
        ('WET', 'WET'),
    ]
    location = models.CharField(max_length=100)
    area_size = models.DecimalField(max_digits=6, decimal_places=2)
    soil_quality = models.CharField(
        max_length=50,
        choices=SOIL_TYPES,
        default='DRY'
    )
    crop=models.ForeignKey(Crop,on_delete=models.CASCADE, related_name='fields',null=True)
    def __str__(self):
        return self.name
    
class Prediction(models.Model):
    REGION_TYPES=[
        ('DESERT','DESERT'),
        ('SEMI ARID','SEMI ARID'),
        ('SEMI HUMID','SEMI HUMID'),
        ('HUMID','HUMID'),
    ]
    WEATHER_TYPES=[
        ('NORMAL','NORMAL'),
        ('SUNNY','SUNNY'),
        ('WINDY','WINDY'),
        ('RAINY','RAINY')
    ]
    REGION = models.CharField(max_length=50,choices=REGION_TYPES,default='DESERT')
    TEMPERATURE=models.IntegerField()
    WEATHER_CONDITION=models.CharField(max_length=50,choices=WEATHER_TYPES,default='NORMAL')
    def __str__(self):
        return self.name
    

class SoilType(models.Model):
    type_name = models.CharField(max_length=50, unique=True)
    water_retention_capacity = models.DecimalField(
        max_digits=5, decimal_places=2)
    permeability_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.type_name


class Land(models.Model):
    location = models.CharField(max_length=100)
    area_size = models.FloatField(default=0)
    soil_type = models.ForeignKey(
    SoilType, on_delete=models.SET_NULL, null=True, related_name='lands')

    def __str__(self):
        return f"{self.location} ({self.area_size} acres)"
