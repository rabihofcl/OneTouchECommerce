from django.urls import path
from . import views


def a(request):
    print('hdslfkj')


urlpatterns = [
    path('', views.admin_signin, name='admin_signin'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('ad_brand_list', views.ad_brand_list, name='ad_brand_list'),
    path('ad_add_brand', views.ad_add_brand, name='ad_add_brand'),
    path('ad_product_list', views.ad_product_list, name='ad_product_list'),
    path('ad_delete_product/', views.ad_delete_product, name='ad_delete_product'),
    path('ad_add_product', views.ad_add_product, name='ad_add_product'),
    path('active_users', views.active_users, name='active_users'),
]