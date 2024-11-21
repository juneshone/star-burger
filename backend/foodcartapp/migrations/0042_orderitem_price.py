# Generated by Django 3.2.15 on 2024-08-13 21:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('foodcartapp', '0041_rename_products_orderitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6,
                                      validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена'),
        ),
    ]