from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from status.serializers import *
from status.models import *

# Create your views here.

class HostsOverview(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = HostSerializer
    queryset = Host.objects.all()

class InfosViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DetailSerializer
    def get_queryset(self):
        queryset = Detail.objects.all()
        host = self.request.query_params.get('host')
        if host is not None:
            queryset = queryset.filter(host=host)
        return queryset

class StatusViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StatusSerializer
    def get_queryset(self):
        queryset = Status.objects.all()
        host = self.request.query_params.get('host')
        if host is not None:
            queryset = queryset.filter(host=host)
        return queryset