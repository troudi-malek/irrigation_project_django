from django.db import models

# Create your models here.


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
