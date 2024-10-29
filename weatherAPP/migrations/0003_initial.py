# Generated by Django 4.1 on 2024-10-25 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('weatherAPP', '0002_delete_weatherdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('temperature', models.FloatField()),
                ('humidity', models.FloatField()),
                ('precipitation', models.FloatField(default=0.0)),
                ('irrigation_need', models.FloatField(default=0.0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
