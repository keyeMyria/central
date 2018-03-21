from django.db import models

# Create your models here.

HOST_STATES = [
    (0,'Disabled'),
    (1,'Down'),
    (2,'Up'),
    (3,'Internet'),
    (4,'Working'),
    (5, 'Up-to-date')
]

class HostStatus(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nom de la machine')
    dns = models.CharField(max_length=255, verbose_name='Nom de domaine')
    ip = models.GenericIPAddressField(verbose_name='Adresse IP')
    description = models.CharField(max_length=2047, verbose_name='Description')
    up = models.BooleanField(verbose_name='Allumé ?', default=False)
    state = models.IntegerField(verbose_name='État', choices=HOST_STATES)
    lastseen = models.DateTimeField(verbose_name='Dernier accès/update', auto_now=True)

class AdditionalInfo(models.Model):
    host = models.ForeignKey(to=HostStatus, on_delete=models.CASCADE, verbose_name='Machine',
                             related_name='infos', null=True)
    title = models.CharField(max_length=1023, verbose_name='Nom de la propriété')
    value = models.CharField(max_length=4095, verbose_name='Description & valeur', blank=True)