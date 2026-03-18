from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sdn_app/api/', include('sdn_app.urls')),
    path('auth/', include('rest_framework.urls')),
]


admin.site.site_header = "SDN Application"
admin.site.site_title = "SDN Application Admin Portal"
admin.site.index_title = "Welcome to SDN Application Portal"
