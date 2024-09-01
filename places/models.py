from django.db import models
from django.utils import timezone


class Place(models.Model):
    address = models.CharField(
        verbose_name='адрес',
        max_length=100,
        unique=True
    )
    lat = models.FloatField(
        verbose_name='широта',
        blank=True,
        null=True
    )
    lon = models.FloatField(
        verbose_name='долгота',
        blank=True,
        null=True
    )
    date_of_update = models.DateTimeField(
        verbose_name='Дата запроса',
        default=timezone.now
    )

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'

    def __str__(self):
        return self.address
