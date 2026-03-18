from sdn_app.models.opendaylight_model import OpenDayLight
import requests

def odl_set_up():

    Response = {"status": False, "message": {}}

    odl_ip = OpenDayLight.objects.all()[0].ip
    odl_port = OpenDayLight.objects.all()[0].port
    username = OpenDayLight.objects.all()[0].username
    password = OpenDayLight.objects.all()[0].password
    url = 'http://' + str(odl_ip) + ':' + str(odl_port) + '/restconf/operational/network-topology:network-topology'

    # Create a requests session with basic authentication
    session = requests.Session()
    session.auth = (username, password)

    try:
        response = session.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        Response["message"] = "Connection to Open Daylight Remote Controller is failed."
        return Response

    Response["status"] = True
    Response["message"] = response.json()
    return Response

