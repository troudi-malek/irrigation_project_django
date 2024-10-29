from django.db import models

# Create your models here.
class PlantType(models.Model):
    plant_type_name = models.CharField(max_length=100)
    plant_type_image = models.ImageField(upload_to='images/irrigation/', null=True, blank=True)
    winter_irrigation_frequency = models.CharField(max_length=20)
    spring_irrigation_frequency = models.CharField(max_length=20)
    summer_irrigation_frequency = models.CharField(max_length=20)
    fall_irrigation_frequency = models.CharField(max_length=20)
    def __str__(self):
        return self.plant_type_name
    
    def plant_count(self):
        return self.plants.count()

class Plant(models.Model):
    name = models.CharField(max_length=100)
    plant_image = models.ImageField(upload_to='images/irrigation/', null=True, blank=True)
    plant_type = models.ForeignKey(PlantType, on_delete=models.CASCADE, related_name='plants')
    sunlight_requirements = models.CharField(max_length=100)
    water_needs = models.CharField(max_length=100)
    growth_rate = models.CharField(max_length=100)

    def __str__(self):
        return self.name
