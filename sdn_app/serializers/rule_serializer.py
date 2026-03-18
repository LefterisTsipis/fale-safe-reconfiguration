from rest_framework import serializers
from sdn_app.models.rule_model import Rule


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'
