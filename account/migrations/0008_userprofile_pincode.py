# Generated by Django 3.2.7 on 2021-10-07 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='pincode',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
