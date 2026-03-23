
from django.core.management import BaseCommand
from django.contrib.auth.models import User
from sdn_app.models.opendaylight_model import OpenDayLight
from sdn_app.models.host_model import Host
import requests
from sdn_app.models.server_model import Server
from sdn_app.helpers.topology_information import topologyInformation



class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print("start init_test_data")
        init_data(self)
        print("end init_test_data")

def get_hosts_and_switches_from_topology(topology):
    switch = []
    hosts= []

    for i in topology["network-topology"]["topology"]:

        if "node" in i:
            for j in i["node"]:
                # Device MAC and IP
                if "host-tracker-service:addresses" in j:
                    for k in j["host-tracker-service:addresses"]:
                        hosts.append(k["ip"])
                else:
                    switch.append(j["node-id"])

    return dict(hosts=hosts, switch=switch)
    
def init_data(self):
    username = 'admin'
    email = 'ccsl@aegean.com'
    password = 'admin'

    # Check if the superuser already exists
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
    else:
        self.stdout.write(self.style.SUCCESS('Superuser already exists.'))

    # Check if the opendaylight model already exists
    if not OpenDayLight.objects.filter(username=username).exists():

        OpenDayLight.objects.create(
            ip='195.251.134.77',
            port=8181,
            username=username,
            password=password
        )
        self.stdout.write(self.style.SUCCESS('OpenDayLight created successfully.'))
    else:
        self.stdout.write(self.style.SUCCESS('OpenDayLight already exists.'))

    """
    try:
        url_topology = 'http://195.251.134.247:8181/restconf/operational/network-topology:network-topology'
        username = 'admin'
        password = 'admin'

        session = requests.Session()
        session.auth = (username, password)

        topology_response = session.get(url_topology)
        topology_response.raise_for_status()
        data = get_hosts_and_switches_from_topology(topology_response.json())

       

        data = topologyInformation(topology_response.json())
    except requests.exceptions.RequestException as e:
        print(str(e))
        return 0

    # Import Hosts
    for ip_address in host_data:
        host, created = Host.objects.get_or_create(ip=ip_address)

    # Import Switches
    for switch_name in switch_data:
        switch, created = Switch.objects.get_or_create(name=switch_name)

    
    host_1 = Host.objects.get(ip="10.0.0.4")
    host_2 = Host.objects.get(ip="10.0.0.3")

    server_1, created = Server.objects.get_or_create(host=host_1)
    server_2, created = Server.objects.get_or_create(host=host_2)

    switch = Switch.objects.get(name="openflow:4")

    server_1_switch_port = int(data["host_port_mapping_to_switch"]["10.0.0.4"])
    server_2_switch_port = int(data["host_port_mapping_to_switch"]["10.0.0.3"])

    ServerSwitchLink.objects.get_or_create(server=server_1,switch=switch, server_port_mapping_to_switch=server_1_switch_port)
    ServerSwitchLink.objects.get_or_create(server=server_2, switch=switch, server_port_mapping_to_switch=server_2_switch_port)
    """




