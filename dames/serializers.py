from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from dames.models import Partie
from uuid import uuid1

class PartieSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['user']
        model = Partie
    def create(self, validated_data):
        user = User.objects.create(username=uuid1())
        Partie.objects.create(**validated_data, user=user)
        token = Token.objects.create(user=user)
        return token.key
