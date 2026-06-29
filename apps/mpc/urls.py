from django.urls import path, include

urlpatterns = [
    path('mpc_orders/', include('apps.mpc.mpc_orders.urls')),
    path('mpc_products/', include('apps.mpc.mpc_products.urls')),
]
