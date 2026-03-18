from django.urls import path

from sdn_app.views.client_servers_roles_view import ClientServersRolesApiView
from sdn_app.views.client_view import ClientListCreateAPIView, ClientRetrieveUpdateDestroyAPIView
from sdn_app.views.fail_secure_reconfiguration_view import BlockCompromisedHostView
from sdn_app.views.get_topology_info_view import GetTopologyInfoApiView, get_topology_ui
from sdn_app.views.rules_view import all_rules_view
from sdn_app.views.server_view import ServerListCreateAPIView, ServerRetrieveUpdateDestroyAPIView
from sdn_app.views.server_view import display_servers
urlpatterns = [
    path('topology/info', GetTopologyInfoApiView.as_view(), name='topology_info'),
    path('client_server_role', ClientServersRolesApiView.as_view(), name='client_server_role_create'),
    path('block-compromised-host/', BlockCompromisedHostView.as_view(), name='block_compromised_host'),

    path('get_topology_ui', get_topology_ui, name='get_topology_ui'),
    path('client_server_role', ClientServersRolesApiView.as_view(), name='client_server_role_create'),

    path('server', ServerListCreateAPIView.as_view(), name='server_list_create'),
    path('server/<int:pk>', ServerRetrieveUpdateDestroyAPIView.as_view(), name='server_retrieve_update_delete'),
    path('servers_ui', display_servers, name='get_servers_ui'),
    path('rules/', all_rules_view, name='all_rules'),  # Map the view to /rules/ URL

    path('client', ClientListCreateAPIView.as_view(), name='server_list_create'),
    path('client/<int:pk>', ClientRetrieveUpdateDestroyAPIView.as_view(), name='server_retrieve_update_delete'),

]
