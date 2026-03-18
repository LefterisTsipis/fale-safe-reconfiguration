from rest_framework import serializers
from sdn_app.models.host_model import Host


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'

