from django.db import models
from app_products.models import Product
from app_users.models import Profile


class OrderPriceConstants(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название константы")
    value = models.FloatField(default=0, verbose_name="Значение")

    class Meta:
        verbose_name = 'Константа'
        verbose_name_plural = 'Константы'


class Order(models.Model):
    EXPRESS = 100
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name="orders", verbose_name="Заказчик")
    createdAt = models.DateTimeField(auto_now_add=True,
                                     verbose_name="Время создания")
    deliveryType = models.CharField(max_length=50, verbose_name="Доставка")
    paymentType = models.CharField(max_length=50, verbose_name="Способ оплаты")
    totalCost = models.FloatField(default=0, verbose_name="Стоимость заказа")
    address = models.CharField(max_length=250, verbose_name="Адрес")
    city = models.CharField(max_length=100, verbose_name="Город")

    STATUS = {
        ("оформление", "оформление"),
        ("ожидание оплаты", "ожидание оплаты"),
        ("готов к получению", "готов к получению"),
        ("завершен", "завершен"),
    }
    status = models.CharField(max_length=50, choices=STATUS,
                              default="оформление", blank=True,
                              verbose_name="Статус заказа")

    class Meta:
        ordering = ('-createdAt',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_total_cost(self):
        result = float(sum(item.get_cost() for item in self.products.all()))
        if self.deliveryType == 'express':
            result += OrderPriceConstants.objects.get(title='EXPRESS_DELIVERY_PRICE').value
        elif result < OrderPriceConstants.objects.get(title='MIN_PRICE_FOR_FREE_DELIVERY').value:
            result += OrderPriceConstants.objects.get(title='DELIVERY_PRICE').value
        return result


class OrderProduct(models.Model):
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE, verbose_name="товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="цена")
    count = models.PositiveIntegerField(default=1, verbose_name="количество")
    order = models.ForeignKey(Order, default=None, on_delete=models.CASCADE,
                              related_name="products", verbose_name="заказ")

    def get_cost(self):
        return self.price * self.count

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Payment(models.Model):
    number = models.CharField(max_length=16, verbose_name="Номер карты")
    name = models.CharField(max_length=128, verbose_name="Имя")
    month = models.CharField(max_length=2, verbose_name="Месяц")
    year = models.CharField(max_length=4, verbose_name="Год")
    code = models.CharField(max_length=3, verbose_name="Код")
    order = models.OneToOneField(Order, on_delete=models.CASCADE,
                                 default=None, related_name="payment")

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплата'
