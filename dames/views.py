import json

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from dames.models import Partie
from dames.serializers import PartieSerializer
from asgiref.sync import async_to_sync
from channels_redis import *
from channels.layers import get_channel_layer
import channels
class PartieViewset(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(Partie.objects.all().values()) #liste les parties

    def post(self, request):
        try:
            partie = Partie.objects.get(user=request.user)
        except Partie.DoesNotExist:
            partie = Partie.objects.create(user=request.user, data=request.data)
        partie.data = self.request.data
        partie.save()
        return Response(request.data, status=201)
    def delete(self, request):
        Partie.objects.get(user=request.user).delete()
        return Response("Partie finie !")

@api_view(http_method_names=['GET'])
def liste(request):
    reponse = []
    for partie in Partie.objects.exclude(player2__gt=''):
            reponse.append({"id":partie.id,
                        "player1": partie.player1})
    return Response(reponse)

@api_view(['POST'])
def rejoindre(request, pk):
    partie = Partie.objects.get(id=pk)
    token = Token.objects.get(user=partie.user)
    partie.player2 = request.data["nom"]
    partie.save()
    print(partie.player2)
    async_to_sync(get_channel_layer().group_send)(  # lance le jeu une fois que les deux joueurs sont co
        "blancs" + str(partie.id),
        {
            'type': 'update_post',
            'data': partie.data
        })
    async_to_sync(get_channel_layer().group_send)(  # lance le jeu une fois que les deux joueurs sont co
        "blancs" + str(partie.id),
        {
            'type': 'update_post',
            'data': "Vous jouez contre "+partie.player2
        })
    return HttpResponse(token.key)

@api_view(['DELETE'])
def delete(request):
    partie = Partie.objects.get(user=request.user)
    Token.objects.get(user=request.user).delete()
    partie.delete()
    request.user.delete()
    return Response("DELETED")

class Lobby(ModelViewSet):
    #queryset = Partie.objects.all()#exclude(player2__gt='')
    serializer_class = PartieSerializer

    def get_queryset(self):
        if self.request.user is not AnonymousUser:
            queryset = Partie.objects.filter(user=self.request.user)
        else:
            queryset = Partie.objects.exclude(player2__gt='')
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = PartieSerializer(data=request.data)
        if serializer.is_valid():
            return HttpResponse(serializer.create(serializer.validated_data))

@api_view(['GET'])
def qui_joue(request):
    partie = Partie.objects.get(user=request.user)
    return HttpResponse(partie.player1_turn)

@api_view(['GET'])
def a_toi(request):
    partie = Partie.objects.get(user=request.user)
    partie.player1_turn = not partie.player1_turn
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "ping_"+str(partie.id),
        {
            'type': 'update',
            'couleur':partie.couleur_joue
         })
    partie.save()
    print(partie.id)
    return HttpResponse(partie.player1_turn)

def test_ws(request):
    #return render(request, 'test.html', {})
    return render(request, 'test_ws.html', {})

@api_view(['GET'])
def id(request):
    print("sent id")
    return HttpResponse(str(Partie.objects.get(user=request.user).id))


class Broadcast(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        msg = self.request.query_params.get('msg')
        async_to_sync(get_channel_layer().group_send)("broadcast",
                                                      {'type': 'update_post',
                                                       'data': str(msg)})
        return Response(msg)
    def post(self, request):
        msg = request.data.get('msg')
        async_to_sync(get_channel_layer().group_send)("broadcast",
                                                      {'type': 'update_post',
                                                       'data': msg})
        return Response(msg)

def admin(request):
    return render(request, 'dames-admin.html',{})