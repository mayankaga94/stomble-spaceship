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
    def get(self, request, format=None):
        spaceships = Spaceship.objects.all()
        serializer = SpaceshipSerializer(spaceships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # Add spaceship
    def post(self, request, format=None):
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

    def put(self, request, id, format=None):
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
    
    def delete(self, request, id, format=None):
        spaceship = self.get_object(id)
        spaceship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LocationListCreateView(APIView):
    """ 
    List all Locations, Create new Location
    """
    def get(self, request, format=None):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data, status=200)
    # Add new location
    def post(self, request, format=None):
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
    #Note: deleting a location will also delete all spaceships at that location
    def delete(self, request, id, format=None):
        location = self.get_object(id)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SpaceshipTravelView(APIView):
    """ 
    Spaceship Travel from Source to Destination
    """
    def put(self, request, spaceship_id, format=None):
        data = request.data
        try:
            # get destination id
            destination_loc = request.data['destination']
            # get spaceship id
            spaceship = Spaceship.objects.get(id=spaceship_id)
            # get location and destination objects
            location = Location.objects.get(id=spaceship.location.id)
            destination = Location.objects.get(id=destination_loc)
        except KeyError:
            return Response({"error": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
        except Spaceship.DoesNotExist:
            return Response({"error": "Spaceship Does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Location.DoesNotExist:
            return Response({"error": "Location Does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if spaceship is operational
        if spaceship.status != "operational":
            return Response({"error": "Spaceship is not operational"})

        # check if location has free hangar space or capacity
        if destination.spaceship_stationed() + 1 > destination.capacity:
            return Response({"error": "Destination spaceport capacity is full"})

        # check if spaceship is located in the same location as destination
        if destination == spaceship.location:
            return Response({"error": "Spaceship already stationed here"})

        # update spaceship location
        spaceship.location = destination
        spaceship.save()
        return Response(spaceship.serialize(), status=status.HTTP_200_OK)