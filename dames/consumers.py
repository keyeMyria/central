# Fichier pour les vues "websocket"
from time import sleep

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from dames.models import Partie

class DamesSync(WebsocketConsumer):
    def connect(self):
        self.id = self.scope["url_route"]["kwargs"]["id"]
        self.couleur = self.scope["url_route"]["kwargs"]["couleur"]
        self.adversaire = "noirs" if self.couleur == "blancs" else "blancs"
        print("accepté un "+self.couleur+", adversaire "+self.adversaire)
        async_to_sync(self.channel_layer.group_add)(self.couleur + self.id, self.channel_name)
        self.partie = Partie.objects.get(id=self.id)
        self.accept()
        #while(self.couleur!=self.partie.couleur_joue): #dans le cas où le 2e peut se co n'import quand
        #    sleep(1)
        #    print(self.partie.couleur_joue)

        #if(self.partie.is_waiting):
        #    sleep(3) #on attend la connection
        #    print("sending")
        #    self.send(text_data=self.partie.data)

    def receive(self, text_data=None, bytes_data=None):
        #self.send(text_data=text_data) #on re-broadcast les nouvelles données à tous les deux
        #self.update_post({'data':text_data}) #on re-broadcast les nouvelles données à tous les deux
        #print(text_data)
        print(self.couleur+" pour "+self.adversaire)
        self.partie.data = text_data
        async_to_sync(self.channel_layer.group_send)(self.adversaire + str(self.id),
                                                      {'type': 'update_post',
                                                       'data': self.partie.data})
        self.partie.save()

    def update_post(self, event):
        print("envoi aux"+self.couleur)
        self.send(text_data=event['data'])

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)("sync_" + self.id, self.channel_name)

class DamesPing(WebsocketConsumer):
    def connect(self):
        self.id = self.scope["url_route"]["kwargs"]["id"] #récup l'id depuis l'url
        async_to_sync(self.channel_layer.group_add)("ping_"+self.id, self.channel_name)
        self.accept()
        self.partie =  Partie.objects.get(id=self.id)
        #self.send(json.dumps({'couleur': self.partie.couleur_joue}))
        self.send(text_data=self.partie.couleur_joue)


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("ping_"+self.id, self.channel_name)

    def update(self, event): #appelé depuis la view, correpond au "type"
        couleur = event["couleur"]
        #self.send(text_data=json.dumps({'couleur': couleur}))
        self.send(text_data=couleur)

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        couleur = json.loads(text_data)["couleur"]
        if couleur == "blancs" or couleur=="noirs":
            booleen = False
            if couleur=="blancs":  booleen = True
            self.partie.player1_turn = booleen
            self.partie.save()
        self.send(text_data=self.partie.couleur_joue)