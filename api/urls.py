from django.urls import path, include

from .views import SpaceshipListCreateView

urlpatterns = [
    path('spaceship', SpaceshipListCreateView.as_view(), name='spaceship-list-create')
]
