from django.db import models


class Host(models.Model):
    ip = models.GenericIPAddressField(null=True, blank=True)
    mac = models.CharField(max_length=17, null=True, blank=True)

    def __str__(self):
        return str(self.ip)
