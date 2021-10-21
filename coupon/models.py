from django.db import models

# Create your models here.


class Coupon(models.Model):
    coupon_name = models.CharField(max_length=100)
    coupon_code = models.CharField(max_length=50, unique=True)
    discount = models.CharField(max_length=50)

    def __str__(self):
        return self.coupon_name