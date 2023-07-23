from django.db import models
from app_products.models import Product
from app_users.models import Profile


class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name="orders")
    createdAt = models.DateTimeField(auto_now_add=True,
                                     verbose_name="Время создания")
    deliveryType = models.CharField(max_length=50, default="", verbose_name="Доставка")
    paymentType = models.CharField(max_length=50, default="", verbose_name="Способ оплаты")
    totalCost = models.FloatField(default=0, verbose_name="Стоимость заказа")
    status = models.CharField(max_length=50, default="", blank=True, verbose_name="Статус заказа")
    address = models.CharField(max_length=250, default="", verbose_name="Адрес")
    city = models.CharField(max_length=100, default="", verbose_name="Город")

    class Meta:
        ordering = ('-createdAt',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.products.all())


class OrderProduct(models.Model):
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(Order, default=None, on_delete=models.CASCADE,
                              related_name="products")

    def get_cost(self):
        return self.price * self.count
