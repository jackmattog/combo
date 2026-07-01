from decimal import Decimal
from rest_framework import serializers
from django.db import transaction
from .models import MpcOrder, MpcOrderItem

class MpcOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpcOrderItem
        # Exclude the 'order' field because it will be linked automatically by the parent
        fields = [
            'id', 'product', 'product_name', 'sku', 'quantity', 
            'unit_price', 'total_price'
        ]
        
        # We lock down these fields so the frontend can ONLY send 'product' and 'quantity'
        read_only_fields = [
            'id', 'product_name', 'sku', 'unit_price', 'total_price'
        ]


class MpcOrderSerializer(serializers.ModelSerializer):
    # This allows us to pass a list of items when creating the order
    items = MpcOrderItemSerializer(many=True)
    
    class Meta:
        model = MpcOrder
        fields = [
            'id', 'order_number', 'user', 'status', 'payment_status', 'payment_method',
            'subtotal', 'tax_amount', 'shipping_fee', 'discount_amount', 'total_amount',
            'shipping_address', 'shipping_city', 'shipping_postal_code', 'shipping_country',
            'created_at', 'updated_at', 'items'
        ]
        
        # The frontend shouldn't dictate the status or totals on creation
        read_only_fields = [
            'id', 'order_number', 'status', 'payment_status', 
            'subtotal', 'tax_amount', 'total_amount', 'created_at', 'updated_at'
        ]

    @transaction.atomic
    def create(self, validated_data):
        """
        Custom create method to handle the nested items securely.
        @transaction.atomic ensures that if any part of the order fails, 
        the entire database transaction rolls back so I don't get partial orders.
        """
        # 1. Extract the nested items data (DRF requires us to handle this manually)
        items_data = validated_data.pop('items')
        
        # 2. We Create the parent MpcOrder first
        order = MpcOrder.objects.create(**validated_data)
        
        subtotal = 0
        
        # 3. Loop through each item the user wants to buy
        for item_data in items_data:
            product_instance = item_data['product']
            quantity = item_data['quantity']
            
            # SECURE DATA FETCH: Pull details directly from our Product model
            unit_price = product_instance.price 
            product_name = product_instance.name 
            sku = getattr(product_instance, 'sku', '') 
            
            # Create the item and link it to the order
            item = MpcOrderItem.objects.create(
                order=order,
                product=product_instance,
                quantity=quantity,
                product_name=product_name,
                sku=sku,
                unit_price=unit_price
            )
            
            # The item's model save() method auto-calculates total_price, so we just add it up
            subtotal += item.total_price 
            
        # 4. Finalize the order financials
        order.subtotal = subtotal
        
        # Calculate the final amount (Subtotal + Shipping - Discounts)
        # Tax will be added here too if I change logic and it requires it
        order.total_amount = (
            subtotal 
            + order.shipping_fee 
            - order.discount_amount
        )
        order.save()
        
        return order