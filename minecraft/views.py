from minecraft.minestat import  MineStat
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

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
