from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from dames.models import Partie


class PartieViewset(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        partie = Partie.objects.get(user=request.user)
        return HttpResponse(partie.data) #si j'utilise Response, DRF mettra des guillements supplémentaire

    def post(self, request):
        try:
            partie = Partie.objects.get(user=request.user)
        except Partie.DoesNotExist:
            partie = Partie.objects.create(user=request.user, data=request.data)
        partie.data = self.request.data
        partie.save()
        return Response(request.data, status=201)

