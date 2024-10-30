from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from UserApp.decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group

@unauthenticated_user
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

def logoutUser(request):
	logout(request)
	return redirect('login')

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'auth/register.html', context)