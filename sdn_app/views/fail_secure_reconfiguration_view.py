from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from sdn_app.helpers.odl_set_up import odl_set_up
from sdn_app.fail_safe_reconfiguration_helpers.set_block_flow_rule import set_block_flow_rule
from sdn_app.fail_safe_reconfiguration_helpers.set_redirect_flow_rule import set_redirect_flow_rule
from sdn_app.helpers.topology_information import topologyInformation
from sdn_app.models.client_model import Client
from sdn_app.models.opendaylight_model import OpenDayLight
from sdn_app.models.rule_model import Rule
from django.shortcuts import get_object_or_404
from sdn_app.models.server_model import Server


class BlockCompromisedHostView(APIView):
    def post(self, request):
        # Get the OpenDayLight information
        odl_ip = OpenDayLight.objects.all()[0].ip
        odl_port = OpenDayLight.objects.all()[0].port
        username = OpenDayLight.objects.all()[0].username
        password = OpenDayLight.objects.all()[0].password
        opendaylight_base_url = 'http://' + str(odl_ip) + ':' + str(odl_port) + '/restconf/'

        # Get the compromised server and check if it exists in the request data
        compromised_server = request.data['compromised_server']
        if not compromised_server:
            return Response("Missing 'compromised_server' in request data.", status=status.HTTP_400_BAD_REQUEST)

        # try to get the server from the database
        try:
            compromised_server = Server.objects.get(host=compromised_server)
        except Server.DoesNotExist:
            return Response({'error': f"Server with id: {compromised_server} is not register in database"},
                            status.HTTP_400_BAD_REQUEST)

        # try to get the topology information
        response = odl_set_up()
        if not response["status"]:
            return Response({"message": response["message"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            topology_data = topologyInformation(response["message"])

        # Get the switch of the compromised server and create the rule_id
        switch_server = topology_data['host_switch_mapping'][compromised_server.host.ip]
        roule_id = compromised_server.host.ip.split('.')[3] + "_" + switch_server.split(':')[1] + "_" + "fale_secure_rule"

        # Check if the rule already exists
        rule = Rule.objects.filter(rule_id=roule_id)
        if rule:
            return Response({'error': f"Rule with id: {roule_id} already exists"}, status.HTTP_400_BAD_REQUEST)

        # Check if the compromised server has a redundant server and create the flow rule
        if compromised_server.server_redundant is None:
            flow_rule_1 = set_block_flow_rule(roule_id, compromised_server)
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            try:
                response = requests.put(
                    opendaylight_base_url + "config/opendaylight-inventory:nodes/node/" + switch_server + "/flow-node-inventory:table/0/flow/" + roule_id,
                    json=flow_rule_1,
                    headers=headers,
                    auth=(username, password),
                )
                if response.status_code == 201:
                    description = f"The SDN application has successfully executed the link shutdown command and the compromised host with IP: {compromised_server.host.ip} has been blocked."
                    Rule.objects.get_or_create(rule_id=roule_id, server=compromised_server, description=description)
                    return Response(
                        {
                            "message": f"The SDN application has successfully executed the link shutdown command and the compromised host with IP: {compromised_server.host.ip} has been blocked.",
                            "rule_id": roule_id},
                        status=status.HTTP_201_CREATED)
                else:
                    return Response(f"Failed to add one or more block rules. Status codes:",
                                    status=status.HTTP_400_BAD_REQUEST)
            except requests.exceptions.RequestException as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            server_redundant = compromised_server.server_redundant
            client = Client.objects.get(server=compromised_server)
            switch_client = topology_data['host_switch_mapping'][client.host.ip]
            src_switch__dst_switch__port = topology_data['src_switch__dst_switch__port'][switch_client+"::"+switch_server]
            flow_rule_2 = set_redirect_flow_rule(roule_id, compromised_server, server_redundant, src_switch__dst_switch__port)
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            try:
                response = requests.put(
                    opendaylight_base_url + "config/opendaylight-inventory:nodes/node/" + switch_client + "/table/0/flow/" + roule_id,
                    json=flow_rule_2,
                    headers=headers,
                    auth=(username, password),
                )
                if response.status_code == 201:
                    description = f"The SDN application has successfully executed the redirect command."
                    Rule.objects.get_or_create(rule_id=roule_id, server=compromised_server, description=description, category="redirect_rule")
                    return Response(
                        {"message": f"The SDN application has successfully executed the redirect command.",
                         "rule_id": roule_id},
                        status=status.HTTP_201_CREATED)
                else:
                    return Response(f"Failed to add one or more block rules. Status codes:",
                                    status=status.HTTP_400_BAD_REQUEST)
            except requests.exceptions.RequestException as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        print("Delete")
        odl_ip = OpenDayLight.objects.all()[0].ip
        odl_port = OpenDayLight.objects.all()[0].port
        username = OpenDayLight.objects.all()[0].username
        password = OpenDayLight.objects.all()[0].password
        opendaylight_base_url = 'http://' + str(odl_ip) + ':' + str(odl_port) + '/restconf/'

        # Get the rule_id and check if it exists in the request data
        rule_id = request.data['rule_id']
        if not rule_id:
            return Response("Missing 'rule_id' in request data.", status=status.HTTP_400_BAD_REQUEST)

        # try to get the rule from the database
        try:
            rule = Rule.objects.get(rule_id=rule_id)
        except Rule.DoesNotExist:
            return Response({'error': "Rule not exists"}, status.HTTP_400_BAD_REQUEST)
        response = odl_set_up()
        if not response["status"]:
            return Response({"message": response["message"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            topology_data = topologyInformation(response["message"])

        server = rule.server
        if rule.category == "blocked_rule":
            switch = topology_data['host_switch_mapping'][server.host.ip]
        else:
            client = Client.objects.get(server=server)
            switch = topology_data['host_switch_mapping'][client.host.ip]
        # Perform the delete request
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = requests.delete(
            opendaylight_base_url + "config/opendaylight-inventory:nodes/node/" + switch + "/flow-node-inventory:table/0/flow/" + rule.rule_id,
            headers=headers,
            auth=(username, password),
        )
        if response.status_code == 200:
            rule = get_object_or_404(Rule, pk=rule.rule_id)
            rule.delete()
            return Response({"Message: Rule deleted succesfully"}, status=status.HTTP_200_OK)
        else:
            return Response(f"Failed to delete one or more block rules. Status codes:",
                            status=status.HTTP_400_BAD_REQUEST)
