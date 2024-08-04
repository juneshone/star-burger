# Generated by Django 3.2.15 on 2024-08-04 20:53

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0039_orderitem_quantity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Элемент заказа', 'verbose_name_plural': 'Элементы заказа'},
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='phonenumber',
            field=phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=128, region='RU', verbose_name='Мобильный номер заказчика'),
        ),
    ]