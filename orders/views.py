from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem, OrderAddress
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer, CreateOrderSerializer
from apps.products.models import SupplierProduct


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        supplier_product_id = request.data.get('supplier_product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            supplier_product = SupplierProduct.objects.get(id=supplier_product_id, is_available=True)
        except SupplierProduct.DoesNotExist:
            return Response({'error': 'Product not available'}, status=status.HTTP_400_BAD_REQUEST)

        if supplier_product.stock_quantity < quantity:
            return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            supplier_product=supplier_product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)


class RemoveFromCartView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateCartItemView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def create_order(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if not cart.items.exists():
        return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CreateOrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Calculate total amount
    total_amount = sum(item.total_price for item in cart.items.all())

    # Create order
    order = Order.objects.create(
        user=request.user,
        total_amount=total_amount,
        notes=serializer.validated_data.get('notes', '')
    )

    # Create order items
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            supplier_product=cart_item.supplier_product,
            quantity=cart_item.quantity,
            unit_price=cart_item.supplier_product.price,
            total_price=cart_item.total_price
        )

        # Update stock
        cart_item.supplier_product.stock_quantity -= cart_item.quantity
        cart_item.supplier_product.save()

    # Create shipping address
    address_data = serializer.validated_data['shipping_address']
    OrderAddress.objects.create(order=order, **address_data)

    # Clear cart
    cart.items.all().delete()

    # Send confirmation email (async)
    from .tasks import send_order_confirmation_email
    send_order_confirmation_email.delay(order.id)

    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)