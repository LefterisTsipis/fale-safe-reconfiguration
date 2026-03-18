from rest_framework import serializers

from sdn_app.models.server_model import Server
from sdn_app.models.client_model import Client

class ClientSerializerReadOnly(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ['ip']
    

class ClientSerializer(serializers.ModelSerializer):
    ip = serializers.ReadOnlyField(source='host.ip')
    
    class Meta:
        model = Client
        fields = '__all__' 


    


