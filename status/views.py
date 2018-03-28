from django.shortcuts import render, redirect
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework import views
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, detail_route, list_route
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
        a = self.request.user
        if self.request.user.is_staff:
            queryset = Status.objects.all()
        else:
            queryset = Status.objects.filter(host__user=self.request.user)
        host = self.request.query_params.get('host')
        if host is not None:
            queryset = queryset.filter(host=host)
        return queryset

    @list_route(methods=['get'])
    def me(self, request):
        me = Host.objects.get(user=request.user)
        return Response(me.pk)

#@permission_classes([permissions.IsAuthenticated])
def me(request):
    pk = Status.objects.get(host__user=request.user).pk
    url = reverse('status-detail', request=request, args={pk})
    return redirect(url)