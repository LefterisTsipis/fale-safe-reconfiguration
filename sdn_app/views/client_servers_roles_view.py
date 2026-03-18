from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sdn_app.helpers.get_hosts_and_switches_from_topology import get_hosts_and_switches_from_topology
from sdn_app.helpers.odl_set_up import odl_set_up
from sdn_app.models.client_model import Client
from sdn_app.models.host_model import Host
from sdn_app.models.server_model import Server
from sdn_app.serializers.client_serializer import ClientSerializer
from sdn_app.serializers.host_serializer import HostSerializer
from sdn_app.serializers.server_serializer import ServerSerializer


class ClientServersRolesApiView(APIView):
    def post(self, request, *args, **kwargs):
        response = odl_set_up()
        if not response["status"]:
            return Response({"message": response["message"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = get_hosts_and_switches_from_topology(response["message"])

            hosts_ip = data["hosts_ip"]
            hosts_mac = data["hosts_mac"]
            servers_ips = request.data['servers_ips']
            clients_ips = request.data['clients_ips']

            # Import Hosts
            for ip_address, mac_address in zip(hosts_ip, hosts_mac):
                host, created = Host.objects.get_or_create(ip=ip_address)
                host.mac = mac_address
                host.save()

            # import Servers
            hosts = Host.objects.filter(ip__in=servers_ips)
            for host in hosts:
                Server.objects.get_or_create(host=host)

            # import clients
            hosts = Host.objects.filter(ip__in=clients_ips)
            for host in hosts:
                Client.objects.get_or_create(host=host)

            # Get all hosts, servers and clients
            hosts = Host.objects.all()
            servers = Server.objects.all()
            clients = Client.objects.all()

            # Serialize the data
            servers_serializer = ServerSerializer(servers, many=True)
            clients_serializer = ClientSerializer(clients, many=True)
            host_serializer = HostSerializer(hosts, many=True)

            # Create the response data
            response_data = {
                "hosts": host_serializer.data,
                "servers": servers_serializer.data,
                "clients": clients_serializer.data,
            }

            # Return the response
            return Response(response_data)
