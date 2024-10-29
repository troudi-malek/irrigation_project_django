from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views import View
from .models import User
from .forms import UserCreationForm  # We'll create this form next

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'Admin/User/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Change this to your desired redirect
        return render(request, 'Admin/User/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Change this to your desired redirect
        else:
            return render(request, 'Admin/User/login.html', {'error': 'Invalid credentials'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')  # Change this to your desired redirect
