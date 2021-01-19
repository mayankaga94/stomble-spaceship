from django.urls import path, include

from .views import (
    SpaceshipListCreateView, 
    LocationListCreateView,
)

urlpatterns = [
    path('spaceship', SpaceshipListCreateView.as_view(), name='spaceship-list-create'),
    path('location', LocationListCreateView.as_view(), name='location-list-create'),
]
