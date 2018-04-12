# Fichier pour les vues "websocket"
import async as async
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from dames.models import Partie

class DamesPing(WebsocketConsumer):
    def connect(self):
        self.id = self.scope["url_route"]["kwargs"]["id"] #récup l'id depuis l'url
        async_to_sync(self.channel_layer.group_add)("ping_"+self.id, self.channel_name)
        self.accept()
        self.partie =  Partie.objects.get(id=self.id)
        self.send(json.dumps({'couleur': self.partie.couleur_joue}))


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("ping_"+self.id, self.channel_name)

    def update(self, event):
        couleur = event["couleur"]
        self.send(text_data=json.dumps({
            'couleur': couleur
        }))
        print(couleur)
    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        couleur = json.loads(text_data)["couleur"]
        if couleur == "blancs" or couleur=="noirs":
            booleen = False
            if couleur=="blancs":  booleen = True
            self.partie.player1_turn = booleen
            self.partie.save()
            self.send(json.dumps({'couleur':self.partie.couleur_joue}))
        else:
            self.send(json.dumps({'couleur':self.partie.couleur_joue}))