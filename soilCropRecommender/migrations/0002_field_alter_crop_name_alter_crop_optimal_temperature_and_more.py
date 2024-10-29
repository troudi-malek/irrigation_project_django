# Generated by Django 4.1 on 2024-10-26 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soilCropRecommender', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('area_size', models.DecimalField(decimal_places=2, max_digits=6)),
                ('soil_quality', models.CharField(choices=[('sandy', 'Sandy'), ('clay', 'Clay'), ('silt', 'Silt'), ('loam', 'Loam'), ('peat', 'Peat'), ('chalk', 'Chalk'), ('gravel', 'Gravel')], default='loam', max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='crop',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='crop',
            name='optimal_temperature',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='crop',
            name='water_need',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]