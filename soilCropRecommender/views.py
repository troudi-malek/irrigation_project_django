from django.shortcuts import render,redirect
from .models import Crop,Field
from .forms import CropForm,FieldForm


def index(request):
    return render(request,'index.html',{})


def Dashboard(request):
    return render(request,'Admin/index.html',{})

def cropFront(request):
    context = {}
    form = FieldForm()
    fields = Field.objects.all()
    context['fields'] = fields

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

    context['form'] = form
    return render(request, 'Client/SoilCrop/soilCropFront.html', context)

def ListCrop(request):
    context={}
    form=CropForm()
    crops=Crop.objects.all()
    context['crops']=crops
    if request.method=='POST':
        if 'save' in request.POST:
            pk=request.POST.get('save')
            if not pk:
                 form = CropForm(request.POST)
            else:
                crop=Crop.objects.get(id=pk)
                form=CropForm(request.POST,instance=crop)
            if form.is_valid():
                form.save()
                form=CropForm()
                return redirect('ListCrop')
        elif 'delete' in request.POST:
            pk=request.POST.get('delete')
            crop=Crop.objects.get(id=pk)
            crop.delete()
        elif 'edit' in request.POST:
             pk=request.POST.get('edit')
             crop=Crop.objects.get(id=pk)
             form=CropForm(instance=crop)
    context['form']=form
    return render(request,'Admin/soilCrop/listSoilCrop.html',context)


# Create your views here.
