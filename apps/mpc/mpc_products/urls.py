from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 1. Initializing  the DefaultRouter
router = DefaultRouter()

# 2. Register ViewSets with the router
router.register(r'categories', views.MpcProductCategoryViewSet, basename='mpc-category')
router.register(r'products', views.MpcProductViewSet, basename='mpc-product')
router.register(r'product-images', views.MpcProductImageViewSet, basename='mpc-product-image')

# 3. Including the router URLs in urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]