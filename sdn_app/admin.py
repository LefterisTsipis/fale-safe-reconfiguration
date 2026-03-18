from django.contrib import admin
from sdn_app.models.opendaylight_model import OpenDayLight
from sdn_app.models.host_model import Host
from sdn_app.models.server_model import Server
from sdn_app.models.client_model import Client
from sdn_app.models.rule_model import Rule

admin.site.register(Server)
admin.site.register(Client)
admin.site.register(Host)
admin.site.register(OpenDayLight)
admin.site.register(Rule)
