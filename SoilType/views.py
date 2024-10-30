from django.shortcuts import get_object_or_404, redirect, render
from .forms import LandForm
from .models import SoilType
from .models import SoilType, Land
from .forms import SoilTypeForm, LandForm
from django.http import JsonResponse
import pandas as pd
# Create your views here.


def index(request):
    return render(request, 'index.html', {})


def Dashboard(request):
    return render(request, 'Admin/index.html', {})


def soil_type_list(request):
    soil_types = SoilType.objects.all()  # Fetch all soil types
    form = SoilTypeForm()  # Initialize an empty form for adding new soil type

    if request.method == 'POST':
        # Check for save action to add a new soil type
        if 'save' in request.POST:
            form = SoilTypeForm(request.POST)
            if form.is_valid():
                form.save()  # Save the new soil type
                return redirect('soil_type_list')  # Redirect to the same view
            else:
                print(form.errors)  # Print errors if the form is not valid

        # Check for edit action to update an existing soil type
        elif 'edit' in request.POST:
            # Get the ID of the soil type to edit
            soil_type_id = request.POST.get('edit')
            # Retrieve the existing soil type
            soil_type = get_object_or_404(SoilType, id=soil_type_id)
            # Bind the form with the instance
            form = SoilTypeForm(request.POST, instance=soil_type)
            if form.is_valid():
                form.save()  # Save the edited soil type
                return redirect('soil_type_list')  # Redirect to the same view
            else:
                print(form.errors)  # Print errors if the form is not valid

        # Check for delete action to remove an existing soil type
        elif 'delete' in request.POST:
            soil_type_id = request.POST.get('delete')
            soil_type = get_object_or_404(SoilType, id=soil_type_id)
            soil_type.delete()  # Delete the soil type
            return redirect('soil_type_list')  # Redirect to the same view

    context = {
        'soil_types': soil_types,
        'form': form,  # Pass the form for rendering
    }
    return render(request, 'Admin/SoilType/listSoilType.html', context)


# Add or Edit a Soil Type


def manage_soil_type(request, pk=None):
    if pk:
        soil_type = get_object_or_404(SoilType, pk=pk)
        form = SoilTypeForm(instance=soil_type)
    else:
        form = SoilTypeForm()

    if request.method == 'POST':
        if pk:
            form = SoilTypeForm(request.POST, instance=soil_type)
        else:
            form = SoilTypeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('list_soil_types')

    context = {'form': form, 'is_editing': pk is not None}
    # Update this line
    return render(request, 'Admin/SoilType/addSoilType.html', context)


# Delete a Soil Type


def delete_soil_type(request, pk):
    soil_type = get_object_or_404(SoilType, pk=pk)
    if request.method == 'POST':
        soil_type.delete()
        return redirect('list_soil_types')
    context = {'soil_type': soil_type}
    return render(request, 'Admin/SoilType/deleteSoilType.html', context)

#############################################
# List all Lands


def list_lands(request):
    lands = Land.objects.all()
    form = LandForm()  # Create an empty form instance for adding new land
    context = {'lands': lands, 'form': form}
    return render(request, 'Client/SoilType/landFront.html', context)
# Add or Edit a Land


def manage_land(request, pk=None):
    if pk:
        land = get_object_or_404(Land, pk=pk)
        form = LandForm(instance=land)
    else:
        form = LandForm()

    if request.method == 'POST':
        form = LandForm(request.POST, instance=land if pk else None)

        if form.is_valid():
            form.save()
            return redirect('land_list')  # Redirect to the land list view

    context = {'form': form, 'is_editing': pk is not None}
    # Ensure correct template is used
    return render(request, 'Client/SoilType/addLand.html', context)


# Delete a Land


def delete_land(request, pk):
    land = get_object_or_404(Land, pk=pk)
    if request.method == 'POST':
        land.delete()  # Delete the land entry
        return redirect('land_list')  # Redirect to the list of lands
