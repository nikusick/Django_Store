from django.db import models
from app_users.models import Profile


class Image(models.Model):
    src = models.ImageField(
        upload_to="static/products/",
        verbose_name="Ссылка",
    )
    alt = models.CharField(max_length=128, default="Продукт", verbose_name="Описание")

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"


class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="Название тэга")


class Specification(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название")
    value = models.CharField(max_length=128, verbose_name="Значение")


class Product(models.Model):
    category = models.PositiveIntegerField(verbose_name="Категория")
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Цена")
    count = models.PositiveIntegerField(verbose_name="Количество")
    date = models.DateTimeField("Дата")
    title = models.CharField(max_length=128, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    fullDescription = models.TextField(blank=True, null=True, verbose_name="Полное описание")
    freeDelivery = models.BooleanField(default=False, verbose_name="Бесплатная доставка")
    images = models.ManyToManyField(Image, related_name="products")
    tags = models.ManyToManyField(Tag, related_name="products")
    specifications = models.ManyToManyField(Specification, related_name="products")
    rating = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Рейтинг")


class Review(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, related_name="author"
    )
    text = models.TextField(verbose_name="Отзыв")
    rate = models.PositiveIntegerField(verbose_name="Оценка")
    date = models.DateTimeField(verbose_name="Дата")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
