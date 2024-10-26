from django.db import models

class Crop(models.Model):
    name=models.CharField(max_length=30)
    water_need=models.DecimalField(max_digits=5,decimal_places=2)
    growth_stage = models.CharField(max_length=50)
    optimal_temperature = models.CharField(max_length=50)


    def __str__(self):
        return self.name

# Create your models here.
