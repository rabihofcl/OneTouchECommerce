from django.urls import path
from . import views


urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('buynow_place_order/', views.buynow_place_order, name='buynow_place_order'),
    path('payments/', views.payments, name='payments'),
    path('buynow_payments/', views.buynow_payments, name='buynow_payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('buynow_order_complete/', views.buynow_order_complete, name='buynow_order_complete'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    


]
