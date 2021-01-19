from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework.views import status

from core.models import Spaceship, Location

class SpaceshipListCreateView(APITestCase):
    def setUp(self) -> None:
        # get url for /api/spaceship
        self.url = reverse('spaceship-list-create',)
        # Create a Location object in test database
        Location.objects.create(
            city="Mumbai",
            planet="Earth",
            capacity=1
        )

    def test_create_spaceship(self):
        self.assertEquals(
            Spaceship.objects.count(),
            0
        )
        data = {
            'name': 'enterprise',
            'model_name': 'stomble101',
            'location': 1,
        }
        # send post request to /api/spaceship to create new spaceship
        response = self.client.post(self.url, data=data, format='json')
        # check response for 201 created
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        
        spaceship = Spaceship.objects.first()
        # Check default status is operational
        self.assertEquals(
            spaceship.status,
            'operational'
        )
        data = {
            'name': 'enterprise2',
            'model_name': 'stomble101',
            'location': 1,
        }
        response = self.client.post(self.url, data=data, format='json')
        # check response when location capacity is full and spaceship is not created
        self.assertEquals(
            Spaceship.objects.count(),
            1
        )

        def test_list_spaceship(self):
            spaceship = Spaceship.objects.create(
                name='enterprise',
                model_name='stomble101',
                location=1
            )
            response = self.client.get(self.url)
            response_json = response.json()
            self.assertEquals(
                response.status_code,
                status.HTTP_200_OK
            )
            self.assertEquals(
                len(response_json),
                1
            )
            data = response_json[0]
            self.assertEquals(
                data['name'],
                spaceship.name
            )
            self.assertEquals(
                data['model_name'],
                spaceship.model_name
            )

class LocationListCreateView(APITestCase):
    def setUp(self) -> None:
        # get url for /api/location
        self.url = reverse('location-list-create',)
        
    def test_create_location(self):
        # check no location objects in test database
        self.assertEquals(
            Location.objects.count(),
            0
        )
        data = {
            'city': 'Sydney',
            'planet': 'Earth',
            'capacity': 3,
        }
        # send post request to /api/location to create new location
        response = self.client.post(self.url, data=data, format='json')
        # check response for 201 created
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        # check database for location
        self.assertEquals(
            Location.objects.count(),
            0
        )

    def test_list_location(self):
        # Create new location object in test database
        location = Location.objects.create(
            city='Sydney',
            planet='Earth',
            capacity=10
        )
        # send get request to retrieve all locations
        response = self.client.get(self.url)
        response_json = response.json()
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            len(response_json),
            1
        )
        data = response_json[0]
        # check location is a match
        self.assertEquals(
            data['city'],
            location.city
        )
        self.assertEquals(
            data['model_name'],
            location.planet
        )