from rest_framework import generics
from sdn_app.models.host_model import Host
from sdn_app.serializers.host_serializer import HostSerializer


class HostListAPIView(generics.ListAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class HostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
