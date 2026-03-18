from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sdn_app.helpers.odl_set_up import odl_set_up
from sdn_app.helpers.topology_information import topologyInformation

from django.shortcuts import render


class GetTopologyInfoApiView(APIView):
    def get(self, request, *args, **kwargs):
        response = odl_set_up()
        if not response["status"]:
            return Response({"message":response["message"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = topologyInformation(response["message"])
        return Response({"data": data})


@login_required
def get_topology_ui(request):
    response = odl_set_up()
    data = topologyInformation(response["message"])
    return render(request, 'display_topology.html', {'json_data': data})
