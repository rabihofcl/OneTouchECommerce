from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.admin_signin, name='admin_signin'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('ad_brand_list/', views.ad_brand_list, name='ad_brand_list'),
    path('ad_delete_brand/', views.ad_delete_brand, name='ad_delete_brand'),
    path('ad_brand_edit/<slug>/', views.ad_brand_edit, name='ad_brand_edit'),
    path('ad_add_brand/', views.ad_add_brand, name='ad_add_brand'),
    path('ad_product_list/', views.ad_product_list, name='ad_product_list'),
    path('ad_product_edit/<id>/', views.ad_product_edit, name='ad_product_edit'),
    path('ad_delete_product/', views.ad_delete_product, name='ad_delete_product'), 
    path('ad_add_product/', views.ad_add_product, name='ad_add_product'),
    path('active_users/', views.active_users, name='active_users'),
    path('blocked_users/', views.blocked_users, name='blocked_users'),
    path('ad_logout/', views.ad_logout, name='ad_logout'),
]


if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # This is nesseccary to access image files on the frontend

# Now when the user visits the base url('http://127.0.0.1:8000/' is case of running locally), 
# the index function from user/views.py file will be called
# name='home' will allows us to redirect the user to this URL by using just this name.
