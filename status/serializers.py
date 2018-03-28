from rest_framework import serializers
from status import models

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Detail
        fields = '__all__'
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Status
        fields = '__all__'
    lastseen = serializers.ReadOnlyField()
    dns = serializers.ReadOnlyField()
    reachable = serializers.ReadOnlyField()

class HostSerializer(serializers.ModelSerializer):
    #def get_queryset(self):
    #    return models.AdditionalInfo.objects.filter(host=self.id)
    class Meta:
        model = models.Host
        fields = '__all__'
        depth = 1
    status = StatusSerializer()
    details = DetailSerializer(many=True)

########################################

class Test:
    def create(self, validated_data):
        infos_data = validated_data.pop('details')
        host = models.Status.objects.create(**validated_data)
        for info_data in infos_data:
            models.Detail.objects.create(host=host, **info_data)
        return host

    def update(self, instance, validated_data):
        infos = validated_data.pop('infos')
        instance.name = validated_data.get('name', instance.name)
        instance.dns = validated_data.get('dns', instance.dns)
        instance.ip = validated_data.get('ip', instance.ip)
        instance.description = validated_data.get('description', instance.description)
        instance.up = validated_data.get('up', instance.up)
        instance.state = validated_data.get('state', instance.state)
        instance.lastseen = validated_data.get('lastseen', instance.lastseen)
        instance.save()
        if len(infos) > 0:
            #new_infos = [info['title'] for info in infos]
            #for info in instance.infos.all():
            #    if info.title not in new_infos:
            #        info.delete()
            for info in instance.details.all():
                info.delete()
            for info in infos:
                models.Detail(**info).save()
        return instance