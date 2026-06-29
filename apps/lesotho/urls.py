from django.urls import path, include

urlpatterns = [
    path('bar_products/', include('apps.lesotho.bar_products.urls')),
    path('bar_orders/', include('apps.lesotho.bar_orders.urls')),
    path('lesotho_carwash/', include('apps.lesotho.lesotho_carwash.urls')),
    path('lodge_rooms/', include('apps.lesotho.lodge_rooms.urls')),
]
