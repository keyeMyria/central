from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from status.serializers import *
from status.models import *

# Create your views here.

class HostsOverview(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HostSerializer
    queryset = HostStatus.objects.all()

class InfosViewSet(viewsets.ModelViewSet):

    serializer_class = InfoSerializer
    def get_queryset(self):
        queryset = AdditionalInfo.objects.all()
        host = self.request.query_params.get('host')
        if host is not None:
            queryset = queryset.filter(host=host)
        return queryset