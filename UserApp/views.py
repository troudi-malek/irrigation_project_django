from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

def Login(request):
    if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')
         user = authenticate(request, username=username, password=password)
         if user is not None:
                 login(request, user)
                 return redirect('client')
         else:
                  messages.info(request, 'Username OR password is incorrect')

    context={}
    return render(request, 'auth/login.html', context)

def logout(request):
     logout(request)
     return redirect('login')

def Register(request):
    form=UserCreationForm()
    if request.method =='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,'account was created for ',context)
            return redirect('login')
    context={'form':form}
    return render(request, 'auth/register.html', context)