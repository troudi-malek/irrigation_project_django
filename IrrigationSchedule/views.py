from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import PlantType, Plant
from .forms import PlantTypeForm, PlantForm, AIRecommendationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def Dashboard(request):
    return render(request,'Admin/index.html',{})

def plant_type_list(request):
    plant_types = PlantType.objects.all() 
    return render(request, 'Admin/IrrigationSchedule/plant_type_list.html',  {'plant_types': plant_types})

def plant_type_create(request):
    if request.method == 'POST':
        form = PlantTypeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('plant_type_list')
    else:
        form = PlantTypeForm()
    return render(request, 'Admin/IrrigationSchedule/plant_type_form.html', {'form': form, 'action': 'Create'})

def plant_type_update(request, pk):
    plant_type = get_object_or_404(PlantType, pk=pk)
    if request.method == 'POST':
        form = PlantTypeForm(request.POST, request.FILES ,instance=plant_type)
        if form.is_valid():
            form.save()
            return redirect('plant_type_list')
    else:
        form = PlantTypeForm(instance=plant_type)
    return render(request, 'Admin/IrrigationSchedule/plant_type_form.html', {'form': form, 'action': 'Update'})


def plant_type_delete(request, pk):
    plant_type = get_object_or_404(PlantType, pk=pk)
    if request.method == 'POST':
        plant_type.delete()
        return redirect('plant_type_list')
    
def your_view(request, plant_type_id):
    # Get the PlantType object using the provided ID
    plant_type = get_object_or_404(PlantType, id=plant_type_id)
    
    
    return render(request, 'your_template.html', {
        'plant_type': plant_type,
        
    })

def plant_list(request, plant_type_id):
    plants = Plant.objects.filter(plant_type_id=plant_type_id)
    return render(request, 'Admin/IrrigationSchedule/plant_list.html', {'plants': plants, 'plant_type_id': plant_type_id})

def plant_create(request, plant_type_id):
    # Get the specified PlantType
    plant_type = get_object_or_404(PlantType, id=plant_type_id)
    
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            # Set the plant's plant_type before saving
            plant = form.save(commit=False)
            plant.plant_type = plant_type
            plant.save()
            return redirect('plant_list', plant_type_id=plant_type.id)
    else:
        # Instantiate an empty form
        form = PlantForm()

    return render(request, 'Admin/IrrigationSchedule/plant_form.html', {'form': form, 'action': 'Create', 'plant_type': plant_type})


def plant_update(request, plant_type_id, pk):
    # Get the specified PlantType and Plant
    plant_type = get_object_or_404(PlantType, request.FILES, id=plant_type_id)
    plant = get_object_or_404(Plant, pk=pk, plant_type=plant_type)  # Ensure the plant belongs to the correct PlantType

    if request.method == 'POST':
        form = PlantForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('plant_list', plant_type_id=plant_type.id)  # Redirect to plant list for this PlantType
    else:
        form = PlantForm(instance=plant)

    return render(request, 'Admin/IrrigationSchedule/plant_form.html', {'form': form, 'action': 'Update', 'plant_type': plant_type})



def plant_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    plant_type_id = plant.plant_type.id
    if request.method == 'POST':
        plant.delete()
        return redirect('plant_list', plant_type_id=plant_type_id)
    return render(request, 'Admin/IrrigationSchedule/plant_confirm_delete.html', {'plant': plant})


def plant_list_filtered(request):
    # Get the filter option from the request (if any)
    plant_type_id = request.GET.get('plant_type')

    # Filter plants by the selected PlantType if provided
    plants = Plant.objects.all()
    if plant_type_id:
        plants = plants.filter(plant_type_id=plant_type_id)

    # Get all plant types for the filter dropdown
    plant_types = PlantType.objects.annotate(plant_count=Count('plants'))

    return render(request, 'Client/IrrigationSchedule/plants.html', {
        'plants': plants,
        'plant_types': plant_types,
        'selected_type': int(plant_type_id) if plant_type_id else None
    })


def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    
    if request.method == 'POST' and request.is_ajax():
        # Process the AJAX request for AI Recommendation
        soil_moisture = request.POST.get('soil_moisture')
        sunlight_hours = request.POST.get('sunlight_hours')
        rainfall_forecast = request.POST.get('rainfall_forecast')
        
        # Example AI recommendation logic
        recommendation = f"Recommended irrigation: {int(float(soil_moisture) * 0.1 + float(sunlight_hours) * 0.05)} liters per week."

        # Send recommendation back as a JSON response
        return JsonResponse({'recommendation': recommendation})

    return render(request, 'Client/IrrigationSchedule/plant_detail.html', {
        'plant': plant,
        'form': AIRecommendationForm(),
    })