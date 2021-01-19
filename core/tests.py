from django.test import TestCase
from app.models import Spaceship, Location

# tests for Location Model
class LocationTest(TestCase):
    def test_location(self):
        self.assertEquals(
            Location.objects.count(),
            0
        )
        
        location = Location.objects.create(
            city="temp_city",
            planet="temp_planet",
            capacity=1
        )
        self.assertEquals(
            Location.objects.count(),
            1
        )

# tests for Spaceship Model
class SpaceshipTest(TestCase):
    def test_spaceship(self):
        self.assertEquals(
            Spaceship.objects.count(),
            0
        )
        location = Location.objects.create(
            city="temp_city",
            planet="temp_planet",
            capacity=5
        )
        spaceship_1 = Spaceship.objects.create(
            name="test_1",
            model_name="test_model_1",
            location=location,
            status="operational"
        )
        spaceship_2 = Spaceship.objects.create(
            name="test_2",
            model_name="test_model_1",
            location=location,
            status="decommissioned"
        )
        self.assertEquals(
            spaceship_2.status,
            'decommissioned'
        )
        self.assertEquals(
            Spaceship.objects.filter(location=location).count(),
            2
        )