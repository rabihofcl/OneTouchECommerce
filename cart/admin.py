from django.contrib import admin
from .models import BuynowItem, Cart, CartItem
# Register your models here.


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(BuynowItem)