from django.db import models
from sdn_app.models.server_model import Server


class Rule(models.Model):
    CATEGORY_CHOICES = [
        ('blocked_rule', 'Blocked Rule'),
        ('redirected_rule', 'Redirected Rule'),
    ]

    category = models.CharField(choices=CATEGORY_CHOICES, default='blocked_rule', max_length=30)
    rule_id = models.CharField(max_length=100, primary_key=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='server_rule', blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.rule_id)