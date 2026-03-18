from django.db import models
from .host_model import Host

class Server(models.Model):
    host = models.OneToOneField(Host, related_name="server", on_delete=models.CASCADE, primary_key=True)
    status = models.BooleanField(default=True)
    server_redundant = models.OneToOneField("self", related_name="server_children", on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.host.ip
