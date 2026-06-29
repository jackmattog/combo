from django.urls import path, include

urlpatterns = [
    path('upmatt_softwares/', include('apps.upmatt.upmatt_softwares.urls')),
    path('web_services/', include('apps.upmatt.web_services.urls')),
]
