# Generated by Django 3.2.7 on 2021-10-23 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_order_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Placed', 'Placed'), ('Accepted', 'Accepted'), ('Shipping', 'Shipping'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Placed', max_length=10),
        ),
    ]
