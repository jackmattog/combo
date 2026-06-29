"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from apps.upmatt import upmatt_softwares

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.shared.core')),
    path('lesotho/bar_products/',include('apps.lesotho.bar_products')),
    path('lesotho/bar_orders/',include('apps.lesotho.bar_orders')),
    path('lesotho/lesotho_carwash/',include('apps.lesotho.lesotho_carwash')),
    path('lesotho/lodge_rooms/',include('apps.lesotho.lodge_rooms')),
    path('mpc/mpc_orders/',include('apps.mpc.mpc_orders')),
    path('mpc/mpc_products/',include('apps.mpc.mpc_products')),
    path('accounts/',include('apps.shared.accounts')),
    path('suggestions/',include('apps.shared.suggestions')),
    path('upmatt/upmatt_softwares/',include('apps.upmatt.upmatt_softwares')),
    path('upmatt/web_services/',include('apps.upmatt.web_services')),
]
