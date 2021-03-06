# Generated by Django 3.2.7 on 2021-10-10 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20211010_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='product_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Shipping', 'Shipping'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Return', 'Return')], default='New', max_length=10),
        ),
    ]
