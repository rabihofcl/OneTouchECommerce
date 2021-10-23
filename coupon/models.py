from django.db import models
from account.models import Account

# Create your models here.


class Coupon(models.Model):
    coupon_name = models.CharField(max_length=100)
    coupon_code = models.CharField(max_length=50, unique=True)
    discount = models.CharField(max_length=50)
    status = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.coupon_name

class CheckCoupon(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.coupon.coupon_name