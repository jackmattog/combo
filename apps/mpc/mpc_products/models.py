from django.db import models
from django.utils.text import slugify

class MpcProductCategory(models.Model):
    mpc_product_category_name = models.CharField(
        max_length=100, 
        unique=True,
        help_text="The unique name of the product category."
    )
    mpc_product_category_slug = models.SlugField(
        max_length=120, 
        unique=True, 
        blank=True,
        help_text="URL-friendly slug. Leaves blank to auto-generate from the name."
    )

    class Meta:
        verbose_name = "MPC Product Category"
        verbose_name_plural = "MPC Product Categories"
        ordering = ['mpc_product_category_name']

    def __str__(self):
        return self.mpc_product_category_name

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to automatically generate 
        a slug from the category name if one isn't explicitly provided.
        """
        if not self.mpc_product_category_slug:
            self.mpc_product_category_slug = slugify(self.mpc_product_category_name)
        super().save(*args, **kwargs)

#Products and products image models

class MpcProduct(models.Model):
    """
    Main model for storing MPC product details.
    """
    class ProductStatus(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        OUT_OF_STOCK = 'OUT_OF_STOCK', 'Out of Stock'
        DRAFT = 'DRAFT', 'Draft / Hidden'

    class UnitChoices(models.TextChoices):
        KILOGRAM = 'kg', 'Kilogram (kg)'
        PIECE = 'pc', 'Piece (pc)'
        LITER = 'L', 'Liter (L)'

    mpc_product_name = models.CharField(
        max_length=200, 
        unique=True
    )
    mpc_product_slug = models.SlugField(
        max_length=220, 
        unique=True, 
        blank=True,
        help_text="Leave blank to auto-generate from product name."
    )
    mpc_product_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Price in TZS."
    )
    mpc_products_status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.AVAILABLE
    )
    mpc_products_category = models.ForeignKey(
        'MpcProductCategory', # Use string reference if defined below, or direct class reference
        on_delete=models.CASCADE,
        related_name='products'
    )
    mpc_product_unit = models.CharField(
        max_length=5,
        choices=UnitChoices.choices,
        default=UnitChoices.PIECE
    )
    mpc_product_details = models.TextField(
        help_text="Detailed description of the product."
    )

    class Meta:
        verbose_name = "MPC Product"
        verbose_name_plural = "MPC Products"
        ordering = ['-id'] # Shows newest products first

    def __str__(self):
        return self.mpc_product_name

    def save(self, *args, **kwargs):
        """Auto-generate slug on save if one isn't provided."""
        if not self.mpc_product_slug:
            self.mpc_product_slug = slugify(self.mpc_product_name)
        super().save(*args, **kwargs)


class MpcProductImage(models.Model):
    """
    Related model to allow multiple images per MPC Product.
    """
    product = models.ForeignKey(
        MpcProduct, 
        on_delete=models.CASCADE, 
        related_name='mpc_products_images'
    )
    image = models.ImageField(
        upload_to='products/images/'
    )
    is_feature_image = models.BooleanField(
        default=False,
        help_text="Check this to make it the primary image for the product."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ['-is_feature_image', '-created_at']

    def __str__(self):
        return f"Image for {self.product.mpc_product_name}"