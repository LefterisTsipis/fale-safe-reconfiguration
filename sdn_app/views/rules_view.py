from sdn_app.models.rule_model import Rule
from django.shortcuts import render

def all_rules_view(request):
    rules = Rule.objects.all()  # Fetch all servers from the database
    return render(request, 'rules.html', {'rules': rules})