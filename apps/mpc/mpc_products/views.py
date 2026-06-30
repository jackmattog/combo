from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Local Models
from .models import MpcProductCategory, MpcProduct, MpcProductImage

# Local Serializers
from .serializers import (
    MpcProductCategorySerializer, 
    MpcProductSerializer, 
    MpcProductImageSerializer
)

# Local Custom Configurations
from .permissions import IsAdminUserOrReadOnly
from .pagination import MpcProductPagination


class MpcProductCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing MPC Product Categories.
    - Guests can Read. Admins can Create/Update/Delete.
    - Not paginated, so the frontend receives a flat list for UI dropdowns.
    """
    queryset = MpcProductCategory.objects.all()
    serializer_class = MpcProductCategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class MpcProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing MPC Products.
    - Guests can Read. Admins can Create/Update/Delete.
    - Uses prefetch_related for database query optimization.
    - Paginated to 30 items per request.
    """
    queryset = MpcProduct.objects.all().prefetch_related('mpc_products_images')
    serializer_class = MpcProductSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = MpcProductPagination


class MpcProductImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing standalone product images.
    - While images are nested in the Product endpoint for reading, 
      this allows admins to upload or delete specific images directly via API.
    """
    queryset = MpcProductImage.objects.all()
    serializer_class = MpcProductImageSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]