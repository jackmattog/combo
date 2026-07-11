import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone

class MpcOrder(models.Model):
    """
    Represents a customer's overall order and its current lifecycle state.
    """
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'

    class PaymentStatus(models.TextChoices):
        UNPAID = 'UNPAID', 'Unpaid'
        PAID = 'PAID', 'Paid'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'

    # Primary keys and identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    
    # Relationships
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='mpc_orders'
    )

    # State tracking
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_method = models.CharField(max_length=50, blank=True, help_text="e.g., Stripe, PayPal, M-Pesa")

    # Financials (I use Decimal as its Currency)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    # Shipping Details (Can also be abstracted to a separate Profile/Address model)
    shipping_address = models.TextField(blank=True)
    shipping_city = models.CharField(max_length=100, blank=True)
    shipping_postal_code = models.CharField(max_length=20, blank=True)
    shipping_country = models.CharField(max_length=100, blank=True)
    
    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'MPC Order'
        verbose_name_plural = 'MPC Orders'

    def __str__(self):
        return f"Order {self.order_number} - {self.user}"

    def save(self, *args, **kwargs):
        # Auto-generate a friendly, readable order number (e.g., ORD-20260701-AB12)
        if not self.order_number:
            date_str = timezone.now().strftime('%Y%m%d')
            uid_str = str(uuid.uuid4()).upper()[:4]
            self.order_number = f"ORD-{date_str}-{uid_str}"
        super().save(*args, **kwargs)


class MpcOrderItem(models.Model):
    """
    Represents an individual line item inside an MpcOrder.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(MpcOrder, on_delete=models.CASCADE, related_name='items')
    
    # We use SET_NULL so if a product is deleted from the database, the historical order is preserved.
    product = models.ForeignKey(
        'mpc_products.MpcProduct',
        on_delete=models.SET_NULL, 
        null=True,
        related_name='order_items'
    )
    
    # Snapshot data: Crucial for historical accuracy if the original product changes
    product_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, blank=True)
    
    quantity = models.PositiveIntegerField(default=1)
    
    # Pricing snapshots
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    class Meta:
        ordering = ['-order__created_at']
        verbose_name = 'MPC Order Item'
        verbose_name_plural = 'MPC Order Items'

    def __str__(self):
        return f"{self.quantity} x {self.product_name} (Order: {self.order.order_number})"

    def save(self, *args, **kwargs):
        # Always dynamically calculate the total price before saving
        if self.unit_price and self.quantity:
            self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)