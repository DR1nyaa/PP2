from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category, SupplierProduct, Supplier
from .serializers import ProductSerializer, CategorySerializer, SupplierProductSerializer, SupplierSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['name', 'created_at', 'price']


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SupplierProductListView(generics.ListAPIView):
    serializer_class = SupplierProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['supplier', 'is_available']
    search_fields = ['product__name', 'product__description']

    def get_queryset(self):
        return SupplierProduct.objects.filter(is_available=True, stock_quantity__gt=0)


class SupplierListView(generics.ListAPIView):
    queryset = Supplier.objects.filter(is_active=True, accepts_orders=True)
    serializer_class = SupplierSerializer