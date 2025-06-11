from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('farmers/', views.farmers, name='farmers'),
    path('products/', views.products, name='products'),
    path('contact/', views.contact, name='contact'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('account/', views.account, name='account'),
    path('register/', views.register_view, name='register'),
]
