from django.urls import path
from . import views

urlpatterns = [

    path('Dashboard/',views.Dashboard),
    path('Dashboard/plant_type_list/', views.plant_type_list, name='plant_type_list'),
    path('Dashboard/plant_type_create/', views.plant_type_create, name='plant_type_create'),
    path('Dashboard/plant_type_update/<int:pk>/', views.plant_type_update, name='plant_type_update'),
    path('plant-types/delete/<int:pk>/', views.plant_type_delete, name='plant_type_delete'),
    path('Dashboard/plants/<int:plant_type_id>/', views.plant_list, name='plant_list'),
    path('plant_type/<int:plant_type_id>/plants/create/', views.plant_create, name='plant_create'),
    path('Dashboard/plants/<int:plant_type_id>/update/<int:pk>/', views.plant_update, name='plant_update'),
    path('Dashboard/plants/delete/<int:pk>/', views.plant_delete, name='plant_delete'),
    path('Client/plants/', views.plant_list_filtered, name='plant_list_filtered'),
    path('Client/plants/<int:pk>/', views.plant_detail, name='plant_detail'),
]

#path('Dashboard/PlantType/',views.PlantTypeList,name='ListCrop'),