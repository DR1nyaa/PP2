from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/items/<int:pk>/', views.UpdateCartItemView.as_view(), name='update-cart-item'),
    path('cart/items/<int:pk>/remove/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/create/', views.create_order, name='create-order'),
]