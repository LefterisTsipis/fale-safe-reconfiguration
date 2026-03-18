from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from sdn_app.models.server_model import Server
from sdn_app.serializers.server_serializer import ServerSerializer


class ServerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer


class ServerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer



@login_required
def display_servers(request):
    servers = Server.objects.all()  # Fetch all servers from the database
    return render(request, 'display_servers.html', {'servers': servers})

@login_required
def report_compromised_server(request):
    if request.method == 'POST':
        compromised_server_id = request.POST.get('compromised_server')
        # Handle the compromised server reporting logic here
        # Example: Log to the database, notify admins, etc.
        return JsonResponse({"status": "success", "message": f"Server {compromised_server_id} reported as compromised."})
    return JsonResponse({"status": "error", "message": "Invalid request method."})