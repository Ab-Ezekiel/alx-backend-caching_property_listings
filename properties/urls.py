# properties/urls.py
from django.urls import path
from .views import property_list

urlpatterns = [
    path('', property_list, name='property_list'),  # will be mounted at /properties/
]
