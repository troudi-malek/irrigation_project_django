from django.shortcuts import get_object_or_404, redirect, render
from .forms import LandForm, SoilTypeForm
from .models import SoilType, Land
from django.http import JsonResponse
import pandas as pd

def index(request):
    return render(request, 'index.html', {})

def Dashboard(request):
    return render(request, 'Admin/index.html', {})

def soil_type_list(request):
    soil_types = SoilType.objects.all()
    form = SoilTypeForm()

    if request.method == 'POST':
        if 'save' in request.POST:
            form = SoilTypeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('soil_type_list')
        elif 'edit' in request.POST:
            soil_type_id = request.POST.get('edit')
            soil_type = get_object_or_404(SoilType, id=soil_type_id)
            form = SoilTypeForm(request.POST, instance=soil_type)
            if form.is_valid():
                form.save()
                return redirect('soil_type_list')
        elif 'delete' in request.POST:
            soil_type_id = request.POST.get('delete')
            soil_type = get_object_or_404(SoilType, id=soil_type_id)
            soil_type.delete()
            return redirect('soil_type_list')

    context = {
        'soil_types': soil_types,
        'form': form,
    }
    return render(request, 'Admin/SoilType/listSoilType.html', context)

def manage_soil_type(request, pk=None):
    soil_type = get_object_or_404(SoilType, pk=pk) if pk else None
    form = SoilTypeForm(instance=soil_type) if pk else SoilTypeForm()

    if request.method == 'POST':
        form = SoilTypeForm(request.POST, instance=soil_type)
        if form.is_valid():
            form.save()
            return redirect('soil_type_list')

    context = {'form': form, 'is_editing': pk is not None}
    return render(request, 'Admin/SoilType/addSoilType.html', context)

def delete_soil_type(request, pk):
    soil_type = get_object_or_404(SoilType, pk=pk)
    if request.method == 'POST':
        soil_type.delete()
        return redirect('soil_type_list')
    context = {'soil_type': soil_type}
    return render(request, 'Admin/SoilType/deleteSoilType.html', context)

def list_lands(request):
    lands = Land.objects.all()
    form = LandForm()
    context = {'lands': lands, 'form': form}
    return render(request, 'Client/SoilType/landFront.html', context)

def manage_land(request, pk=None):
    land = get_object_or_404(Land, pk=pk) if pk else None
    form = LandForm(instance=land) if pk else LandForm()

    if request.method == 'POST':
        form = LandForm(request.POST, instance=land)
        if form.is_valid():
            form.save()
            return redirect('land_list')

    context = {'form': form, 'is_editing': pk is not None}
    return render(request, 'Client/SoilType/addLand.html', context)

def delete_land(request, pk):
    land = get_object_or_404(Land, pk=pk)
    if request.method == 'POST':
        land.delete()
        return redirect('land_list')
    context = {'land': land}
    return render(request, 'Client/SoilType/deleteLand.html', context)
