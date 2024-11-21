# Generated by Django 3.2.15 on 2024-08-15 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0046_auto_20240815_0008'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='payment',
            field=models.CharField(choices=[('CASH', 'Наличные'), ('ELECTRONIC', 'Электронно')], db_index=True, default='CASH', max_length=50, verbose_name='Способ оплаты'),
        ),
    ]