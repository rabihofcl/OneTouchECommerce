"""onetouch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('mainadmin/', admin.site.urls),
    path('admin/', include('admin_panel.urls')),
    path('', views.home, name='home'),
    path('signin', views.signin,name='signin'),
    path('phone_login', views.phone_login, name='phone_login'),
    path('phone_login_otp', views.phone_login_otp, name='phone_login_otp'),
    path('register', views.register,name='register'),
    path('otp_register', views.otp_register, name='otp_register'),
    path('signout', views.signout, name='signout'),
    path('store', views.store, name='store'),
    path('store/<slug:brand_slug>/', views.store, name='product_by_brand'),
    path('store/<slug:brand_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('cart/', include('cart.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
