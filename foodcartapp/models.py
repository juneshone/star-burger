from django.db import models
from django.db.models import F, Sum
from django.core.validators import MinValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderDetail(models.Model):
    firstname = models.CharField('Имя', max_length=100)
    lastname = models.CharField('Фамилия', max_length=100)
    phonenumber = PhoneNumberField(
        'Мобильный номер заказчика',
        region="RU",
        db_index=True,
    )
    address = models.TextField('Адрес доставки', max_length=200)
    STATUS_CHOICES = [
        ('UNPROCESSED', 'Необработанный'),
        ('CONFIRMATION', 'Готовится'),
        ('ASSEMBLED', 'Собран'),
        ('ON_WAY', 'В пути'),
        ('DELIVERED', 'Доставлен'),
        ('CANCELLED', 'Отменен'),
    ]
    status = models.CharField(
        'Статус заказа',
        max_length=50,
        choices=STATUS_CHOICES,
        default='UNPROCESSED',
        db_index=True,
    )
    comment = models.TextField(
        'Комментарий к заказу',
        max_length=300,
        blank=True,
    )
    registered_at = models.DateTimeField(
        'Зарегистрирован в',
        default=timezone.now,
        db_index=True,
    )
    called_at = models.DateTimeField(
        'Время звонка',
        null=True,
        blank=True,
        db_index=True,
    )
    delivered_at = models.DateTimeField(
        'Дата доставки',
        null=True,
        blank=True,
        db_index=True,
    )
    PAYMENT_CHOICES = [
        ('CASH', 'Наличные'),
        ('ELECTRONIC', 'Электронно'),
    ]
    payment = models.CharField(
        'Способ оплаты',
        max_length=50,
        choices=PAYMENT_CHOICES,
        default='CASH',
        db_index=True,
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='order_details',
        verbose_name='Ресторан',
        db_index=True,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname}, {self.address}, {self.status}'


class OrderCostQuerySet(models.QuerySet):
    def calculate_order_cost(self):
        order_cost = Sum(F('order_items__price') * F('order_items__quantity'))
        return order_cost


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Товар',
        db_index=True,
    )
    order = models.ForeignKey(
        OrderDetail,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Детали заказа',
        db_index=True,
    )
    quantity = models.PositiveIntegerField(
        'Количество',
        default=1
    )
    price = models.DecimalField(
        'Цена',
        validators=[MinValueValidator(0)],
        max_digits=6,
        decimal_places=2,
    )
    objects = OrderCostQuerySet.as_manager()

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f'{self.product} ({self.order})'
