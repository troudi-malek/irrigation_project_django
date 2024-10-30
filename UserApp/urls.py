from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.Login, name='login'),
    path('logout/', views.logoutUser, name='logout'),
]
