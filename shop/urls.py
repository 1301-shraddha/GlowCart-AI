from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),

    path('checkout/', views.checkout, name='checkout'),

    # 👇 Ye 2 lines add karo
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),

    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),
    path("ai-recommend/", views.ai_recommend, name="ai_recommend"),
]