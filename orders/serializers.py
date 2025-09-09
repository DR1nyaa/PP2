from rest_framework import serializers
from .models import Order, OrderItem, OrderAddress, Cart, CartItem
from apps.products.serializers import SupplierProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_details = SupplierProductSerializer(source='supplier_product', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='supplier_product.product.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier_product.supplier.company_name', read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = OrderAddressSerializer(read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class CreateOrderSerializer(serializers.Serializer):
    shipping_address = OrderAddressSerializer()
    notes = serializers.CharField(required=False, allow_blank=True)