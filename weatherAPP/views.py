# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .service import get_weather_data, calculate_irrigation_needs
from .models import WeatherData
from .forms import WeatherDataForm




def fetch_weather(request):
    weather_data = None
    irrigation_need = None
    error = None

    if request.method == "POST":
        city = request.POST.get('city', 'London')  # Default to 'London' if not provided
        weather_data = get_weather_data(city)

        if weather_data:
            # Calculate irrigation need from weather data
            irrigation_need = calculate_irrigation_needs(weather_data)

            WeatherData.objects.create(
                city=city,
                temperature=weather_data['main']['temp'],
                humidity=weather_data['main']['humidity'],
                precipitation=weather_data.get('rain', {}).get('1h', 0),
                irrigation_need=irrigation_need
            )

      
        else:
            error = 'Could not fetch weather data.'

    return render(request, 'Admin/Weather/AddWeather.html', {
        'weather_data': weather_data,
        'irrigation_need': irrigation_need,
        'error': error,
    })
    
    
    
    
def weather_list(request):
    weather_data = WeatherData.objects.all()
    return render(request, 'Admin/Weather/home.html', {'weather_data': weather_data})


def delete_weather(request, id):
    weather = get_object_or_404(WeatherData, id=id)
    weather.delete()
    return redirect('weather_list')  # Redirect to the list view
  
  
  
def update_weather(request, id):
    weather = get_object_or_404(WeatherData, id=id)
    if request.method == 'POST':
        form = WeatherDataForm(request.POST, instance=weather)
        if form.is_valid():
            form.save()
            return redirect('weather_list')  # Redirect after successful save
    else:
        form = WeatherDataForm(instance=weather)

    return render(request, 'Admin/Weather/update_weather.html', {'form': form, 'weather': weather})


def irrigation_plan_list(request):
    irrigation_plans = IrrigationPlan.objects.all()
    return render(request, 'Admin/IrrigationPlan/home.html', {'irrigation_plans': irrigation_plans})

def add_irrigation_plan(request):
    if request.method == 'POST':
        form = IrrigationPlanForm(request.POST)
        if form.is_valid():
            weather_data = form.cleaned_data['weather_data']
            water_amount = calculate_irrigation_needs({
                'main': {
                    'temp': weather_data.temperature,
                    'humidity': weather_data.humidity
                },
                'rain': {
                    '1h': weather_data.precipitation
                }
            })
            irrigation_plan = form.save(commit=False)
            irrigation_plan.water_amount = water_amount  # Calculate water amount
            irrigation_plan.save()
            return redirect('irrigation_plan_list')  # Redirect to the list view
    else:
        form = IrrigationPlanForm()

    weather_data_list = WeatherData.objects.all()
    return render(request, 'Admin/IrrigationPlan/add_irrigation_plan.html', {
        'form': form,
        'weather_data_list': weather_data_list
    })

def update_irrigation_plan(request, id):
    irrigation_plan = get_object_or_404(IrrigationPlan, id=id)
    if request.method == 'POST':
        form = IrrigationPlanForm(request.POST, instance=irrigation_plan)
        if form.is_valid():
            form.save()
            return redirect('irrigation_plan_list')  # Redirect after successful save
    else:
        form = IrrigationPlanForm(instance=irrigation_plan)

    return render(request, 'Admin/IrrigationPlan/update_irrigation_plan.html', {'form': form, 'irrigation_plan': irrigation_plan})

def delete_irrigation_plan(request, id):
    irrigation_plan = get_object_or_404(IrrigationPlan, id=id)
    irrigation_plan.delete()
    return redirect('irrigation_plan_list')  # Redirect to the list view