from .forms import LandForm
from .forms import SoilTypeForm
from .models import SoilType
from django.shortcuts import render, redirect, get_object_or_404
from .models import Crop, Field, Prediction, Land, SoilType
from .forms import CropForm, FieldForm, PredictionForm, SoilTypeForm, LandForm
from .models import SoilType, Land
from .forms import SoilTypeForm, LandForm
from django.shortcuts import get_object_or_404
from .forms import LandForm  # You'll need to create this form
from .models import Land, SoilType
from django.shortcuts import render, redirect
from .models import Crop, Field,Prediction ,Land ,SoilType
from .forms import CropForm, FieldForm,PredictionForm , SoilTypeForm ,LandForm
from django.http import JsonResponse
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder
from django.conf import settings
from django.http import HttpResponse
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib
import matplotlib.pyplot as plt

def index(request):
    return render(request, 'index.html', {})

def Dashboard(request):
    return render(request, 'Admin/index.html', {})

def cropFront(request):
    context = {}
    form = FieldForm()
    fields = Field.objects.all()
    context['fields'] = fields
    showpredict=False
    showvalue=False
    formpredict=PredictionForm()
    if request.method == 'POST':
        if 'save' in request.POST:
            form = FieldForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('CropFront')

        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            field = Field.objects.get(id=pk)
            field.delete()
            return redirect('CropFront')

        elif 'update' in request.POST:
            pk = request.POST.get('update')
            field = Field.objects.get(id=pk)
            formupdate = FieldForm(instance=field)
            context['editing_field'] = field.id
            context['formupdate'] = formupdate

        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            field = Field.objects.get(id=pk)
            formupdate = FieldForm(request.POST, instance=field)
            if formupdate.is_valid(): 
                formupdate.save()
                return redirect('CropFront')
            else:
                context['formupdate'] = formupdate
                context['editing_field'] = field.id
        elif 'predict' in request.POST:
            pk = request.POST.get('predict')
            showpredict=True
            context['showpredict']=showpredict
            field = Field.objects.get(id=pk)
            context['editing_field'] = field.id
            context['formpredict'] = formpredict
        elif 'SendPrediction' in request.POST:
            pk = request.POST.get('SendPrediction')
            showpredict = False
            field = Field.objects.get(id=pk)
            formpredict = PredictionForm(request.POST)
            if formpredict.is_valid():
                temperature = formpredict.cleaned_data.get('TEMPERATURE')
                Region=formpredict.cleaned_data.get('REGION')
                Weather_condition=formpredict.cleaned_data.get('WEATHER_CONDITION')
                soiltype=field.soil_quality
                croptype=field.crop
                result=load_data(request,temperature,Region,Weather_condition,soiltype,croptype)
                predicted_water_requirement = result['predicted_water_requirement']
                context['predicted_water_requirement']=predicted_water_requirement
                showvalue=True
                context['showvalue']=showvalue
            else:
                context['formpredict'] = formpredict
    context['form'] = form
    return render(request, 'Client/SoilCrop/soilCropFront.html', context)

def ListCrop(request):
    context = {}
    form = CropForm()
    crops = Crop.objects.all()
    context['crops'] = crops
    if request.method == 'POST':
        if 'save' in request.POST:
            pk = request.POST.get('save')
            if not pk:
                form = CropForm(request.POST)
            else:
                crop = Crop.objects.get(id=pk)
                form = CropForm(request.POST, instance=crop)
            if form.is_valid():
                form.save()
                form = CropForm()
                return redirect('ListCrop')
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            crop = Crop.objects.get(id=pk)
            crop.delete()
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            crop = Crop.objects.get(id=pk)
            form = CropForm(instance=crop)
    context['form'] = form
    return render(request, 'Admin/soilCrop/listSoilCrop.html', context)

def load_data(request,temperature,Region,Weather_condition,soiltype,croptype):
    dataset_path = os.path.join(os.path.dirname(__file__), 'data', 'DATASET - Sheet1.csv')

    try:
        data = pd.read_csv(dataset_path)

        def expand_temperature_range(row):
            temp_str = row['TEMPERATURE']
            if '-' in temp_str:
                lower, upper = map(int, temp_str.split('-'))
                expanded_rows = []
                for temp in range(lower, upper + 1):
                    new_row = row.copy()
                    new_row['TEMPERATURE'] = temp
                    expanded_rows.append(new_row)
                return pd.DataFrame(expanded_rows)
            else:
                row['TEMPERATURE'] = float(temp_str)
                return row.to_frame().T

        expanded_data = pd.concat([expand_temperature_range(row) for _, row in data.iterrows()], ignore_index=True)

        expanded_data = pd.get_dummies(expanded_data, columns=['CROP TYPE', 'SOIL TYPE', 'REGION', 'WEATHER CONDITION'])

        X = expanded_data.drop('WATER REQUIREMENT', axis=1)
        y = expanded_data['WATER REQUIREMENT'] 

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print(f"Mean Squared Error: {mse}")

        importance = model.coef_
        features = X.columns
        feature_importance = pd.DataFrame({'Feature': features, 'Importance': importance})
        feature_importance = feature_importance.sort_values(by='Importance', ascending=False)
        print(feature_importance)

        joblib.dump(model, os.path.join(settings.MEDIA_ROOT, 'linear_regression_model.pkl'))

        crop_types = ['BANANA', 'BEAN', 'CABBAGE', 'CITRUS', 'COTTON']
        soil_types = ['loamy', 'sandy', 'clay']  
        regions = ['region1', 'region2']  
        weather_conditions = ['sunny', 'rainy', 'cloudy'] 
        fake_data = pd.DataFrame({
            'CROP TYPE': [croptype],
            'SOIL TYPE': [soiltype],
            'REGION': [Region],
            'TEMPERATURE': [temperature],
            'WEATHER CONDITION': [Weather_condition]
        })
        fake_data = pd.get_dummies(fake_data).reindex(columns=X.columns, fill_value=0)
        fake_prediction = model.predict(fake_data)
        predicted_water_requirement = fake_prediction[0]
        print("fake_prediction",fake_prediction)
        print("predicted_water_requirement",predicted_water_requirement)
        return {
        'predicted_water_requirement': predicted_water_requirement,
        'data': expanded_data  # Include any additional data needed
    }

    except Exception as e:
        return HttpResponse(f"An error occurred while loading the dataset: {str(e)}")


#########################################################################


def index(request):
    return render(request, 'index.html', {})


def Dashboard(request):
    return render(request, 'Admin/index.html', {})


def cropFront(request):
    context = {}
    form = FieldForm()
    fields = Field.objects.all()
    context['fields'] = fields
    showpredict = False
    showvalue = False
    formpredict = PredictionForm()
    if request.method == 'POST':
        if 'save' in request.POST:
            form = FieldForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('CropFront')

        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            field = Field.objects.get(id=pk)
            field.delete()
            return redirect('CropFront')

        elif 'update' in request.POST:
            pk = request.POST.get('update')
            field = Field.objects.get(id=pk)
            formupdate = FieldForm(instance=field)
            context['editing_field'] = field.id
            context['formupdate'] = formupdate

        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            field = Field.objects.get(id=pk)
            formupdate = FieldForm(request.POST, instance=field)
            if formupdate.is_valid():
                formupdate.save()
                return redirect('CropFront')
            else:
                context['formupdate'] = formupdate
                context['editing_field'] = field.id
        elif 'predict' in request.POST:
            pk = request.POST.get('predict')
            showpredict = True
            context['showpredict'] = showpredict
            field = Field.objects.get(id=pk)
            context['editing_field'] = field.id
            context['formpredict'] = formpredict
        elif 'SendPrediction' in request.POST:
            pk = request.POST.get('SendPrediction')
            showpredict = False
            field = Field.objects.get(id=pk)
            formpredict = PredictionForm(request.POST)
            if formpredict.is_valid():
                temperature = formpredict.cleaned_data.get('TEMPERATURE')
                Region = formpredict.cleaned_data.get('REGION')
                Weather_condition = formpredict.cleaned_data.get(
                    'WEATHER_CONDITION')
                soiltype = field.soil_quality
                croptype = field.crop
                result = load_data(request, temperature, Region,
                                   Weather_condition, soiltype, croptype)
                predicted_water_requirement = result['predicted_water_requirement']
                context['predicted_water_requirement'] = predicted_water_requirement
                showvalue = True
                context['showvalue'] = showvalue
            else:
                context['formpredict'] = formpredict
    context['form'] = form
    return render(request, 'Client/SoilCrop/soilCropFront.html', context)


def ListCrop(request):
    context = {}
    form = CropForm()
    crops = Crop.objects.all()
    context['crops'] = crops
    if request.method == 'POST':
        if 'save' in request.POST:
            pk = request.POST.get('save')
            if not pk:
                form = CropForm(request.POST)
            else:
                crop = Crop.objects.get(id=pk)
                form = CropForm(request.POST, instance=crop)
            if form.is_valid():
                form.save()
                form = CropForm()
                return redirect('ListCrop')
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            crop = Crop.objects.get(id=pk)
            crop.delete()
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            crop = Crop.objects.get(id=pk)
            form = CropForm(instance=crop)
    context['form'] = form
    return render(request, 'Admin/soilCrop/listSoilCrop.html', context)


def load_data(request, temperature, Region, Weather_condition, soiltype, croptype):
    dataset_path = os.path.join(os.path.dirname(
        __file__), 'data', 'DATASET - Sheet1.csv')

    try:
        data = pd.read_csv(dataset_path)

        def expand_temperature_range(row):
            temp_str = row['TEMPERATURE']
            if '-' in temp_str:
                lower, upper = map(int, temp_str.split('-'))
                expanded_rows = []
                for temp in range(lower, upper + 1):
                    new_row = row.copy()
                    new_row['TEMPERATURE'] = temp
                    expanded_rows.append(new_row)
                return pd.DataFrame(expanded_rows)
            else:
                row['TEMPERATURE'] = float(temp_str)
                return row.to_frame().T

        expanded_data = pd.concat([expand_temperature_range(
            row) for _, row in data.iterrows()], ignore_index=True)

        expanded_data = pd.get_dummies(expanded_data, columns=[
                                       'CROP TYPE', 'SOIL TYPE', 'REGION', 'WEATHER CONDITION'])

        X = expanded_data.drop('WATER REQUIREMENT', axis=1)
        y = expanded_data['WATER REQUIREMENT']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print(f"Mean Squared Error: {mse}")

        importance = model.coef_
        features = X.columns
        feature_importance = pd.DataFrame(
            {'Feature': features, 'Importance': importance})
        feature_importance = feature_importance.sort_values(
            by='Importance', ascending=False)
        print(feature_importance)

        joblib.dump(model, os.path.join(
            settings.MEDIA_ROOT, 'linear_regression_model.pkl'))

        crop_types = ['BANANA', 'BEAN', 'CABBAGE', 'CITRUS', 'COTTON']
        soil_types = ['loamy', 'sandy', 'clay']
        regions = ['region1', 'region2']
        weather_conditions = ['sunny', 'rainy', 'cloudy']
        fake_data = pd.DataFrame({
            'CROP TYPE': [croptype],
            'SOIL TYPE': [soiltype],
            'REGION': [Region],
            'TEMPERATURE': [temperature],
            'WEATHER CONDITION': [Weather_condition]
        })
        fake_data = pd.get_dummies(fake_data).reindex(
            columns=X.columns, fill_value=0)
        fake_prediction = model.predict(fake_data)
        predicted_water_requirement = fake_prediction[0]
        print("fake_prediction", fake_prediction)
        print("predicted_water_requirement", predicted_water_requirement)
        return {
            'predicted_water_requirement': predicted_water_requirement,
            'data': expanded_data  # Include any additional data needed
        }

    except Exception as e:
        return HttpResponse(f"An error occurred while loading the dataset: {str(e)}")

#########################################################################
# List all Soil Types


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
