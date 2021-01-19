from django.shortcuts import render
from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from app.models import Spaceship, Location
from .serializers import SpaceshipSerializer, LocationSerializer

class SpaceshipCreateList(APIView):
    # List all spaceships
    def get(self, request):
        spaceships = Spaceship.objects.all()
        serializer = SpaceshipSerializer(spaceships, many=True)
        return Response(serializer.data, status=200)
    # Add spaceship
    def post(self, request):
        serializer = SpaceshipSerializer(data=request.data)
        if serializer.is_valid():
            location = serializer.validated_data.get('location')
            if location.spaceship_stationed() == location.capacity:
                return Response({"error": "Location has no space to store spaceship"},status=status.HTTP_200_OK)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)