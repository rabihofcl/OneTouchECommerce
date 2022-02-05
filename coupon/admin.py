from django.contrib import admin
from . models import Coupon, CheckCoupon

# Register your models here.

admin.site.register(Coupon)
admin.site.register(CheckCoupon)