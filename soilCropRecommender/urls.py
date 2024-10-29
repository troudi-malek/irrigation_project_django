from django.urls import path
from . import views

urlpatterns = [
    path('client',views.index),
    path('client/SoilCrop',views.cropFront,name='CropFront'),
    path('Dashboard/',views.Dashboard),
    path('Dashboard/ListCrop/',views.ListCrop,name='ListCrop'),
    path('train-model/', views.load_data, name='train_model'),
]