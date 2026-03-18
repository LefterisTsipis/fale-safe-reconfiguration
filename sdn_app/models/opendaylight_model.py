from django.db import models


class OpenDayLight(models.Model):
    ip = models.GenericIPAddressField(null=True, blank=True)
    port = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.ip
