from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name="cart"),
    path('add_product/<int:product_id>/', views.add_product_to_cart, name="add_product_to_cart"),
    path('remove_product/<int:product_id>/<int:remove_completely>/', views.remove_product_from_cart, name="remove_product_from_cart"),
]