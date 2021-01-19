from django.urls import path, include

from .views import (
    SpaceshipListCreateView, 
    LocationListCreateView,
    SpaceshipDetailView,
)

urlpatterns = [
    path('spaceship', SpaceshipListCreateView.as_view(), name='spaceship-list-create'),
    path('spaceship/<int:id>', SpaceshipDetailView.as_view(), name='spaceship-detail'),
    path('location', LocationListCreateView.as_view(), name='location-list-create'),
]
