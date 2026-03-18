from rest_framework import generics
from sdn_app.models.rule_model import Rule
from sdn_app.serializers.rule_serializer import RuleSerializer


class RuleListAPIView(generics.ListAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
