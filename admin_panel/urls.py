from os import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.admin_signin, name='admin_signin'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('ad_brand_list', views.ad_brand_list, name='ad_brand_list'),
    path('ad_delete_brand', views.ad_delete_brand, name='ad_delete_brand'),
    path('ad_brand_edit/<slug>', views.ad_brand_edit, name='ad_brand_edit'),
    path('ad_add_brand', views.ad_add_brand, name='ad_add_brand'),
    path('ad_product_list', views.ad_product_list, name='ad_product_list'),
    path('ad_product_edit/<id>', views.ad_product_edit, name='ad_product_edit'),
    path('ad_delete_product', views.ad_delete_product, name='ad_delete_product'), 
    path('ad_add_product', views.ad_add_product, name='ad_add_product'),
    path('active_users', views.active_users, name='active_users'),
    path('block_user/<id>/', views.block_user, name='block_user'),
    path('blocked_users', views.blocked_users, name='blocked_users'),
    path('activate_user/<id>/', views.activate_user, name='activate_user'),
    path('ad_logout', views.ad_logout, name='ad_logout'),
    path('ad_active_orders',views.ad_active_orders, name='ad_active_orders'),
    path('ad_past_orders',views.ad_past_orders, name='ad_past_orders'),
    path('ad_order_edit/<order_number>/', views.ad_order_edit, name='ad_order_edit'),
    path('change_status/<id>', views.change_status, name='change_status'),
    path('ads', views.ads, name='ads'),
    path('ad_add_ads', views.ad_add_ads, name='ad_add_ads'),
    path('delete_ads', views.delete_ads, name='delete_ads'),
    path('report', views.report, name='report'),
    path('brand_export_csv', views.brand_export_csv, name='brand_export_csv'),
    path('brand_export_excel', views.brand_export_excel, name='brand_export_excel'),
    path('brand_export_pdf', views.brand_export_pdf, name='brand_export_pdf'),
    path('product_export_csv', views.product_export_csv, name='product_export_csv'),
    path('product_export_excel', views.product_export_excel, name='product_export_excel'),
    path('product_export_pdf', views.product_export_pdf, name='product_export_pdf'),
    path('order_export_csv', views.order_export_csv, name='order_export_csv'),
    path('order_export_excel', views.order_export_excel, name='order_export_excel'),
    path('order_export_pdf', views.order_export_pdf, name='order_export_pdf'),
    path('coupon', views.coupon, name='coupon'),
    path('add_coupon', views.add_coupon, name='add_coupon'),

    
]


if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # This is nesseccary to access image files on the frontend

# Now when the user visits the base url('http://127.0.0.1:8000/' is case of running locally), 
# the index function from user/views.py file will be called
# name='home' will allows us to redirect the user to this URL by using just this name.
