from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.mpc.mpc_products.models import MpcProductCategory, MpcProduct
from django.urls import reverse

User = get_user_model()

class MpcProductAPITests(APITestCase):
    
    def setUp(self):
        """
        I am prepping the database with users and a product so I can test 
        different API requests against them.
        """
        # 1. Create a staff/admin user
        self.admin_user = User.objects.create_user(
            username="daddy_admin", 
            password="testpassword123", 
            is_staff=True
        )
        
        # 2. Create a regular customer user
        self.regular_user = User.objects.create_user(
            username="customer", 
            password="testpassword123", 
            is_staff=False
        )
        
        # 3. Create dummy product data
        self.category = MpcProductCategory.objects.create(mpc_product_category_name="Tools")
        self.product = MpcProduct.objects.create(
            mpc_product_name="Hoe",
            mpc_product_price=15000.00,
            mpc_products_category=self.category,
            mpc_product_details="Farming tool."
        )
        
        # Setup the URL endpoint mapped by our DefaultRouter
        self.product_list_url = reverse('mpc-product-list')

    def test_public_user_can_read_products(self):
        """
        I am testing that an anonymous IP address (guest) gets a 200 OK status
        and can see the paginated product list for the frontend catalog.
        """
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Checking if my custom pagination is wrapping the data correctly
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)

    def test_public_user_cannot_create_product(self):
        """
        I want to make absolutely sure unauthenticated users are blocked 
        from adding products to my database.
        """
        payload = {
            "mpc_product_name": "Stolen Item",
            "mpc_product_price": "100.00",
            "mpc_products_category": self.category.id,
            "mpc_product_details": "Should fail."
        }
        response = self.client.post(self.product_list_url, data=payload)
        
        # They should get a 401 Unauthorized or 403 Forbidden
        self.assertTrue(response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_admin_user_can_create_product(self):
        """
        I am logging in as the staff user to verify that the custom 
        permission allows me to POST new data successfully.
        """
        # Force authentication with the admin account I created in setUp()
        self.client.force_authenticate(user=self.admin_user)
        
        payload = {
            "mpc_product_name": "New Tractor Part",
            "mpc_product_price": "120000.00",
            "mpc_products_category": self.category.id,
            "mpc_product_details": "Genuine part.",
            "mpc_product_unit": "pc"
        }
        response = self.client.post(self.product_list_url, data=payload)
        
        # 201 means "Created successfully"
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MpcProduct.objects.count(), 2) # Hoe + Tractor Part