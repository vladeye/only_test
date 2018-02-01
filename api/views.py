from django.shortcuts import render
from rest_framework import generics
from .serializers import ReadingsSerializer
from .models import Readings


class CreateView(generics.ListCreateAPIView):
    """This class defines the create behaviour of our rest api"""
    queryset = Readings.objects.all()
    serializer_class = ReadingsSerializer

    def perform_create(selfself, serializer):
        """Save the post data when creating a new reading"""
        serializer.save()

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Readings.objects.all()
    serializer_class = ReadingsSerializer
