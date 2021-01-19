from django.urls import path, include

from .views import (
    SpaceshipListCreateView, 
    LocationListCreateView,
    SpaceshipDetailView,
    LocationDetailView,
    SpaceshipTravelView,
)

urlpatterns = [
    path('spaceship', SpaceshipListCreateView.as_view(), name='spaceship-list-create'),
    path('spaceship/<int:id>', SpaceshipDetailView.as_view(), name='spaceship-detail'),
    path('spaceship/travel/<int:spaceship_id>', SpaceshipTravelView.as_view(), name='spaceship-travel'),
    path('location', LocationListCreateView.as_view(), name='location-list-create'),
    path('location/<int:id>', LocationDetailView.as_view(), name='location-detail'),
]
