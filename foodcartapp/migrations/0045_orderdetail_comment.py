# Generated by Django 3.2.15 on 2024-08-14 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_orderdetail_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='comment',
            field=models.TextField(blank=True, max_length=300, verbose_name='Комментарий к заказу'),
        ),
    ]
