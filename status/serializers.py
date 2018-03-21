from rest_framework import serializers
from status import models

class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdditionalInfo
        fields = '__all__'

class HostSerializer(serializers.ModelSerializer):
    #def get_queryset(self):
    #    return models.AdditionalInfo.objects.filter(host=self.id)
    class Meta:
        model = models.HostStatus
        fields = '__all__'
        depth = 1
    lastseen = serializers.ReadOnlyField()
    infos = InfoSerializer(many=True)

    def create(self, validated_data):
        infos_data = validated_data.pop('infos')
        host = models.HostStatus.objects.create(**validated_data)
        for info_data in infos_data:
            models.AdditionalInfo.objects.create(host=host, **info_data)
        return host

    def update(self, instance, validated_data):
        infos_data = validated_data.pop('infos')
        host = models.HostStatus.objects.update(**validated_data)
        #il faut itérer l'instance pour savoir quoi modifier/ ...
        #for info_data in infos_data:
        #    id = int(infos_data.pop('id'))
        #    models.AdditionalInfo.objects.update(host=host, pk=id, **info_data)
        return host