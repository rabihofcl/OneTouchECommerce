from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_signin, name='admin_signin'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('active_users', views.active_users, name='active_users')
]