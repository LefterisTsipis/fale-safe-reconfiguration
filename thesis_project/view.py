from django.http import HttpResponse

def index(request):
    return HttpResponse("""
        <h1>RESPOND</h1>
        <a href="/sdn_app/api/get_topology_ui">Topology UI</a><br>
        <a href="/sdn_app/api/servers_ui">Servers UI</a><br>
        <a href="/admin">Admin</a>
    """)