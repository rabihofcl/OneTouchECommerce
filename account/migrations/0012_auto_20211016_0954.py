# Generated by Django 3.2.7 on 2021-10-16 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20211014_0711'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='phone_number_1',
            new_name='phone_number',
        ),
        migrations.RemoveField(
            model_name='address',
            name='phone_number_2',
        ),
        migrations.AddField(
            model_name='address',
            name='email',
            field=models.EmailField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
