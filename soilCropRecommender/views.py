from django.shortcuts import render


def index(request):
    return render(request,'index.html',{})


def amine(request):
    return render(request,'Admin/index.html',{})


# Create your views here.
