from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('remove_cart/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('remove_item/', views.remove_item, name='remove_item'),
    path('add_item/', views.add_item, name='add_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('buy_now/<id>/', views.buy_now, name='buy_now'),
]