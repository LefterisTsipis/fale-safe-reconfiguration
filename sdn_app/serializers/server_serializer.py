from rest_framework import serializers
from sdn_app.models.server_model import Server


class ServerSerializer(serializers.ModelSerializer):
    ip = serializers.ReadOnlyField(source='host.ip')
    mac = serializers.ReadOnlyField(source='host.mac')
    class Meta:
        model = Server
        fields = ['host', 'ip', 'mac', 'server_redundant', 'status']
        # fields = '__all__'

        

"""
class ServerSerializer_v2(serializers.ModelSerializer):
    network_functions_names = serializers.SerializerMethodField()
    ip = serializers.ReadOnlyField(source='host.ip')

    class Meta:
        model = Server
        fields = '__all__'

    def get_network_functions_names(self, obj):
        network_functions = obj.network_function_server.all().values_list('name')
        return (network_functions)
"""