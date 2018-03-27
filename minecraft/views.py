from minecraft.minestat import  MineStat
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
@api_view(['get'])
def minecraft_status(request):
    mc = MineStat('ribes.me', 53)
    if mc.online:
        print(mc.motd)
        return Response({
            "up":True,
            "motd":''.join(mc.motd.split('\u0000')),
            "players":mc.current_players,
            "max":mc.max_players})
    else:
        return Response({'detail':'Offline',
            "up":False}, status=500)

@api_view(['get']) #définit une vue gérée par DRF, et permet d'utiliser Response
def hello_world(request):
    return Response({"message":"Hello World !"})