from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Partie(models.Model):
    data = models.CharField(max_length=2048, verbose_name='Données JSON')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
