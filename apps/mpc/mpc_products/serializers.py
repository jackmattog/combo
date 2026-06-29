from rest_framework import serializers
from .models import MpcProductCategory, MpcProduct, MpcProductImage

class MpcProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for handling product images.
    """
    class Meta:
        model = MpcProductImage
        fields = ['id', 'image', 'is_feature_image']


class MpcProductCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for product categories.
    """
    class Meta:
        model = MpcProductCategory
        fields = ['id', 'mpc_product_category_name', 'mpc_product_category_slug']


class MpcProductSerializer(serializers.ModelSerializer):
    """
    Main product serializer nesting images and category details 
    for an optimized frontend consumption experience.
    """
    # 1. Nesting images: 'mpc_products_images' matches the related_name on the model ForeignKey
    mpc_products_images = MpcProductImageSerializer(many=True, read_only=True)
    
    # 2. Advanced Pattern: Nesting category details for READ operations
    category_details = MpcProductCategorySerializer(source='mpc_products_category', read_only=True)

    class Meta:
        model = MpcProduct
        fields = [
            'id',
            'mpc_product_name',
            'mpc_product_slug',
            'mpc_product_price',
            'mpc_products_status',
            'mpc_product_unit',
            'mpc_product_details',
            'mpc_products_category',  # PrimaryKey field used for WRITE operations (POST/PUT)
            'category_details',        # Nested object field used for READ operations (GET)
            'mpc_products_images',     # Nested array of images
        ]
        
    def validate_mpc_product_price(self, value):
        """
        Business logic validation ensuring prices are never zero or negative.
        """
        if value <= 0:
            raise serializers.ValidationError("Product price must be greater than zero.")
        return value