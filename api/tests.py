from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework.views import status

from app.models import Spaceship, Location

class SpaceshipListCreateView(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('api-spaceship-list',)
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
            'op'
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
                spaceship.title
            )
            self.assertEquals(
                data['model_name'],
                spaceship.text
            )