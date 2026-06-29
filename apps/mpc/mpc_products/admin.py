from django.contrib import admin
from .models import MpcProductCategory, MpcProduct, MpcProductImage

@admin.register(MpcProductCategory)
class MpcProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('mpc_product_category_name', 'mpc_product_category_slug')
    search_fields = ('mpc_product_category_name',)
    # Automatically fills the slug in the admin panel as I type the name
    prepopulated_fields = {'mpc_product_category_slug': ('mpc_product_category_name',)}


class MpcProductImageInline(admin.TabularInline):
    """
    Allows managing images directly inside the Product admin page.
    """
    model = MpcProductImage
    extra = 3  # Displays 3 empty image upload slots by default
    fields = ('image', 'is_feature_image')


@admin.register(MpcProduct)
class MpcProductAdmin(admin.ModelAdmin):
    # Columns displayed in the main product table list
    list_display = (
        'mpc_product_name', 
        'mpc_products_category', 
        'mpc_product_price', 
        'mpc_product_unit', 
        'mpc_products_status'
    )
    
    # Sidebar filters for quick navigation
    list_filter = ('mpc_products_status', 'mpc_products_category', 'mpc_product_unit')
    
    # Fields that can be typed into the search bar
    search_fields = ('mpc_product_name', 'mpc_product_details')
    
    # Automatically fills the slug field in the form as you type the product name
    prepopulated_fields = {'mpc_product_slug': ('mpc_product_name',)}
    
    # Attaches the image inline manager to this product form
    inlines = [MpcProductImageInline]