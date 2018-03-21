from django.shortcuts import render
from rest_framework import viewsets

from status.serializers import *
from status.models import *

# Create your views here.

class HostsOverview(viewsets.ModelViewSet):
    serializer_class = HostSerializer
    queryset = HostStatus.objects.all()