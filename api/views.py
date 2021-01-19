from django.shortcuts import render
from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import Spaceship, Location
from .serializers import SpaceshipSerializer, LocationSerializer

class SpaceshipListCreateView(APIView):
    """ 
    List all Spaceships, Add new Spaceship
    """
    def get(self, request):
        spaceships = Spaceship.objects.all()
        serializer = SpaceshipSerializer(spaceships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # Add spaceship
    def post(self, request):
        serializer = SpaceshipSerializer(data=request.data)
        if serializer.is_valid():
            location = serializer.validated_data.get('location')
            # Check if number of spaceship stationed at this location is equal to location capacity
            if location.spaceship_stationed() == location.capacity:
                return Response({"error": "Location has no space to store spaceship"},status=status.HTTP_200_OK)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpaceshipDetailView(APIView):
    """ 
    Update Spaceship Status, Delete Spaceship
    """
    def get_object(self, id):
        try:
            return Spaceship.objects.get(id=id)
        except Spaceship.DoesNotExist:
            raise Http404

    def put(self, request, id):
        spaceship = self.get_object(id)
        try:
            spaceship_status = {'status':request.data['status']}
        except KeyError:
            return Response({"status":["Invalid Data"]}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SpaceshipSerializer(spaceship,data=spaceship_status, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        spaceship = self.get_object(id)
        spaceship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LocationListCreateView(APIView):
    """ 
    List all Locations, Create new Location
    """
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data, status=200)
    # Add new location
    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocationDetailView(APIView):
    """ 
    Delete Location
    """
    def get_object(self, id):
        try:
            return Location.objects.get(id=id)
        except Location.DoesNotExist:
            raise Http404

    def delete(self, request, id):
        location = self.get_object(id)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)