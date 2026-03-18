from django.db import models
from sdn_app.models.host_model import Host
from sdn_app.models.server_model import Server


class Client(models.Model):
    host = models.OneToOneField(Host, related_name="client", on_delete=models.CASCADE, primary_key=True)
    server = models.ManyToManyField(Server, related_name="client", blank=True, symmetrical=False)

    def __str__(self):
        return self.host.ip
