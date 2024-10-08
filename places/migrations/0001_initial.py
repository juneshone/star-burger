# Generated by Django 3.2.15 on 2024-08-31 18:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100, unique=True, verbose_name='адрес')),
                ('lat', models.FloatField(blank=True, null=True, verbose_name='широта')),
                ('lon', models.FloatField(blank=True, null=True, verbose_name='долгота')),
                ('date_of_update', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата запроса')),
            ],
            options={
                'verbose_name': 'место',
                'verbose_name_plural': 'места',
            },
        ),
    ]
