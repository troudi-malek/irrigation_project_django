from django.urls import path
from . import views

urlpatterns = [
    path('client',views.index),
    path('Dashboard/',views.Dashboard),
    path('Dashboard/ListCrop/',views.ListCrop,name='ListCrop'),
    

]