from django.test import TestCase
from apps.mpc.mpc_products.models import MpcProductCategory, MpcProduct, MpcProductImage

class MpcProductModelTests(TestCase):
    
    def setUp(self):
        """
        I am setting up baseline data that will run before every single test.
        This saves me from having to create a category in every individual test function.
        """
        self.category = MpcProductCategory.objects.create(
            mpc_product_category_name="Livestock Feed"
        )

    def test_category_slug_is_auto_generated(self):
        """
        I want to make sure that if I don't provide a slug, my overridden save() 
        method generates one correctly.
        """
        self.assertEqual(self.category.mpc_product_category_slug, 'livestock-feed')

    def test_product_creation_and_slug(self):
        """
        I am verifying that a product can be created and linked to the category,
        and that its slug is also auto-generated.
        """
        product = MpcProduct.objects.create(
            mpc_product_name="Starter Mash 50kg",
            mpc_product_price=47000.00,
            mpc_products_category=self.category,
            mpc_product_details="Food for chicks."
        )
        # Verify the database recorded it correctly
        self.assertEqual(product.mpc_product_slug, 'starter-mash-50kg')
        self.assertEqual(product.mpc_products_status, 'AVAILABLE') # Checking default value
        
    def test_product_image_relationship(self):
        """
        I need to ensure the One-to-Many foreign key relationship is working,
        so I can confidently loop through images on the Next.js frontend.
        """
        product = MpcProduct.objects.create(
            mpc_product_name="Dairy Meal",
            mpc_product_price=20000.00,
            mpc_products_category=self.category,
            mpc_product_details="Milk booster."
        )
        
        # Creating two mock images for this single product
        MpcProductImage.objects.create(product=product, image="mock_front.jpg", is_feature_image=True)
        MpcProductImage.objects.create(product=product, image="mock_back.jpg")
        
        # If the related_name 'mpc_products_images' works, this should equal 2
        image_count = product.mpc_products_images.count()
        self.assertEqual(image_count, 2)