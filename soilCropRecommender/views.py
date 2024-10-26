from django.shortcuts import render,redirect
from .models import Crop
from .forms import CropForm


def index(request):
    return render(request,'index.html',{})


def Dashboard(request):
    return render(request,'Admin/index.html',{})

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
