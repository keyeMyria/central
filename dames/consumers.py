# Fichier pour les vues "websocket"
from time import sleep

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from django.forms import model_to_dict

from dames.models import Partie

class DamesSync(WebsocketConsumer):
    def connect(self):
        self.id = self.scope["url_route"]["kwargs"]["id"]
        self.couleur = self.scope["url_route"]["kwargs"]["couleur"]
        self.adversaire = "noirs" if self.couleur == "blancs" else "blancs"
        print("accepté un "+self.couleur+", adversaire "+self.adversaire)
        async_to_sync(self.channel_layer.group_add)(self.couleur + self.id, self.channel_name)
        async_to_sync(self.channel_layer.group_add)("broadcast", self.channel_name) #
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
        async_to_sync(self.channel_layer.group_send)(self.adversaire + str(self.id),#pour activer l'interface admin
                                                      {'type': 'update_post',
                                                       'data': self.partie.data})
        self.partie.save()
        print(self.partie.data)

    def update_post(self, event):
        print("envoi aux"+self.couleur)
        self.send(text_data=event['data'])
        async_to_sync(self.channel_layer.group_send)("admin" + str(self.id),
                                                     {'type': 'sync',
                                                      'data': self.partie.data})

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.couleur + self.id, self.channel_name)
        async_to_sync(self.channel_layer.group_discard)("broadcast", self.channel_name)

class DamesAdmin(WebsocketConsumer):
    def connect(self):
        self.id = self.scope['url_route']['kwargs']['id']
        async_to_sync(self.channel_layer.group_add)("admin"+self.id, self.channel_name)
        self.accept()
        self.send(text_data=json.dumps(model_to_dict(Partie.objects.get(pk=self.id))))

    def sync(self, event):
        print(event)
        #self.send(text_data=json.dumps(event['data']))
        self.send(text_data=json.dumps(model_to_dict(Partie.objects.get(pk=self.id))))

    def receive(self, text_data=None, bytes_data=None):
        partie = Partie.objects.get(pk=text_data)
        self.send(json.dumps(partie))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)("admin"+self.id, self.channel_name)
        self.send(text_data="au revoir")
