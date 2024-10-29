from django.urls import path
from . import views

urlpatterns = [
    path('client',views.index),
    path('client/SoilCrop',views.cropFront,name='CropFront'),
    path('Dashboard/',views.Dashboard),
    path('Dashboard/ListCrop/',views.ListCrop,name='ListCrop'),
    path('train-model/', views.load_data, name='train_model'),
    #################################################################################
    # Land URLs under Client
    path('client/lands/', views.list_lands, name='land_list'),
    path('client/lands/add/', views.manage_land, name='add_land'),
    path('client/lands/edit/<int:pk>/', views.manage_land, name='edit_land'),
    path('client/lands/delete/<int:pk>/',
         views.delete_land, name='delete_land'),
    # Soil Type URLs under Dashboard
    path('Dashboard/soil-types/', views.soil_type_list,
         name='soil_type_list'),  # List all soil types
    path('Dashboard/soil-types/manage/', views.manage_soil_type,
         name='add_soil_type'),  # Adding new soil type
    path('Dashboard/soil-types/edit/<int:pk>/', views.manage_soil_type,
         name='edit_soil_type'),  # Editing existing soil type
    path('Dashboard/soil-types/delete/<int:pk>/', views.delete_soil_type,
         name='delete_soil_type'),  # Deleting soil type
    
]