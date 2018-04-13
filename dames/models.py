from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Partie(models.Model):
    data = models.CharField(max_length=4096, verbose_name='Données JSON', blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    player1 = models.CharField(max_length=255, verbose_name="Joueur des blancs", blank=True)
    player2 = models.CharField(max_length=255, verbose_name="Joueur des noirs", blank=True)
    player1_turn= models.BooleanField(verbose_name="C'est au tour des blancs", default=True)

    @property
    def is_waiting(self):
        if len(self.player2)==0:
            return True
        else: return False

    def __str__(self):
        return self.player1 +" "+ self.player2
    @property
    def couleur_joue(self):
        if not self.player1_turn: return "blancs"
        else: return "noirs"