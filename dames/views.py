from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
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
        partie = Partie.objects.get(user=request.user)
        return HttpResponse(partie.data) #si j'utilise Response, DRF mettra des guillements supplémentaire

    def post(self, request):
        try:
            partie = Partie.objects.get(user=request.user)
        except Partie.DoesNotExist:
            partie = Partie.objects.create(user=request.user, data=request.data)
        partie.data = self.request.data
        #async_to_sync(get_channel_layer().send("ping-"+partie.id, {"a_toi":partie.player1_turn,
        #                                                                           "data":partie.data}))
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
    return render(request, 'test_ws.html', {})

@api_view(['GET'])
def id(request):
    print("sent id")
    return HttpResponse(str(Partie.objects.get(user=request.user).id))