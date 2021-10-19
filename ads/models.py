from django.db import models

from brand.models import Brand
from product.models import Product

# Create your models here.


class Ads(models.Model):
    banner_name = models.CharField(max_length=100, unique=True)
    banner = models.ImageField(upload_to='photos/ads')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.banner_name


    