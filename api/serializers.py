from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.models import Spaceship, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'city', 'planet', 'capacity']

        validators = [
            UniqueTogetherValidator(
                queryset=Location.objects.all(),
                fields=['city', 'planet']
            )
        ]

class SpaceshipSerializer(serializers.ModelSerializer):
    # location = LocationSerializer(required=True)
    class Meta:
        model = Spaceship
        fields = ['id', 'name', 'model_name', 'location', 'status']