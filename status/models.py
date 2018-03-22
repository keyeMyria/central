from django.db import models
from django.contrib.auth.models import User
# Create your models here.

HOST_STATES = [
    (0,'Disabled'),
    (1,'Down'),
    (2,'Up'),
    (3,'Internet'),
    (4,'Working'),
    (5, 'Up-to-date')
]
CHASSIS = [
    ('rack'  ,'Serveur Rack'),
    ('tower' ,'Format Tour'),
    ('laptop','Ordinateur portable')
]
USE_CASE = [
    ('personal','Personal'),
    ('family','PC familial'),
    ('server','Serveur')
]
POWER_ACTIONS = [
    ('none', 'Non disponible'),
    ('start', 'Démarrer'),
    ('reboot', 'Redémarrer'),
    ('poweroff','Éteindre et Allumer, redémarrer'),
    ('suspend', 'Veille et démarrer'),
    ('rtcwake', 'Arrêt temporaire')
]
class Host(models.Model):
    class Meta:
        verbose_name = 'Machine'
    description = models.CharField(max_length=2047, verbose_name='Description')
    dns = models.CharField(max_length=255, verbose_name='Nom de domaine')
    name = models.CharField(max_length=255, verbose_name='Nom de la machine')
    chassis = models.CharField(verbose_name='Chassis', choices=CHASSIS, max_length=255) #physique
    use_case = models.CharField(verbose_name="Type d'utilisation", choices=USE_CASE, max_length=255)
    power_action = models.CharField(choices=POWER_ACTIONS, verbose_name='Gestion de l\'alimentation',
                                    max_length=255) #actions d'alimentations disponibles/possibles
    #user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='API user')
    def __str__(self):
        return self.name+' ('+self.dns+') - '+self.use_case +' '+self.chassis
    def state(self):
        return self.status.state
    def ip(self):
        return self.status.ip
    def statut(self):
        return self.status

class Status(models.Model):
    class Meta:
        verbose_name_plural = 'Status des machines'
        verbose_name = 'Status'
    host = models.OneToOneField(to=Host, verbose_name='Machine', related_name='status', on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(verbose_name='Adresse IP')
    up = models.BooleanField(verbose_name='Allumé ?', default=False)
    state = models.IntegerField(verbose_name='État', choices=HOST_STATES)
    lastseen = models.DateTimeField(verbose_name='Dernier accès/update', auto_now=True)
    remote_capable = models.BooleanField(verbose_name='Accès à distance possible')

    def __str__(self):
        return self.host.name+' - '+self.host.dns+' ('+str(self.ip)+'), '+HOST_STATES[self.state][1]

class Detail(models.Model):
    class Meta:
        verbose_name = 'Détails machine'
    def __str__(self):
        return self.title+' ('+str(self.host)+')'
    host = models.ForeignKey(to=Host, on_delete=models.CASCADE, verbose_name='Machine',
                             related_name='details', null=True)
    title = models.CharField(max_length=1023, verbose_name='Nom de la propriété')
    value = models.CharField(max_length=4095, verbose_name='Description & valeur', blank=True)
