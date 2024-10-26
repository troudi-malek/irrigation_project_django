from django.db import models

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    precipitation = models.FloatField(default=0.0)
    irrigation_need = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WeatherData for {self.city} at {self.timestamp}"


class IrrigationPlan(models.Model):
    weather_data = models.OneToOneField(WeatherData, on_delete=models.CASCADE, related_name="irrigation_plan")
    water_amount = models.FloatField(help_text="Water amount in liters needed based on current weather.")
    frequency = models.CharField(
        max_length=50,
        choices=[("daily", "Daily"), ("weekly", "Weekly"), ("biweekly", "Biweekly")],
        default="daily",
        help_text="Frequency of irrigation based on weather data."
    )
    start_time = models.TimeField(help_text="Time of day to start irrigation.")
    duration = models.IntegerField(help_text="Duration of irrigation in minutes.")
    
    def __str__(self):
        return f"Irrigation Plan for {self.weather_data.city} on {self.weather_data.timestamp.date()}"

    class Meta:
        verbose_name = "Irrigation Plan"
        verbose_name_plural = "Irrigation Plans"
