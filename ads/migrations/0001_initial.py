# Generated by Django 3.2.7 on 2021-10-18 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0003_product_image4'),
        ('brand', '0003_alter_brand_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_name', models.CharField(max_length=100, unique=True)),
                ('banner', models.ImageField(upload_to='photos/ads')),
                ('brand', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='brand.brand')),
                ('product', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
