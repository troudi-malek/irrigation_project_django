from django.urls import path
from . import views

urlpatterns = [
    path('client',views.index),
    path('amine/',views.amine)

]