import datetime

from django.db import models
from app_users.models import Profile


class Image(models.Model):
    src = models.ImageField(
        upload_to="static/products/",
        verbose_name="Ссылка",
    )
    alt = models.CharField(max_length=128, default="Фото", verbose_name="Описание")

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"

    def __str__(self):
        return str(self.src)


class Category(models.Model):
    title = models.CharField(max_length=128)
    image = models.ForeignKey(Image, null=True, on_delete=models.CASCADE)
    parent_category = models.ForeignKey('self', null=True, blank=True,
                                        related_name='subcategories',
                                        on_delete=models.CASCADE, verbose_name='Родительская категория')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        if self.parent_category is not None:
            return f'{self.parent_category} -> {self.title}'
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name="Название тэга")

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name


class Specification(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название")
    value = models.CharField(max_length=128, verbose_name="Значение")

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"

    def __str__(self):
        return f'{self.name} ( {self.value} )'


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="Категория",
                                 on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Цена")
    count = models.PositiveIntegerField(verbose_name="Количество")
    date = models.DateTimeField("Дата")
    title = models.CharField(max_length=128, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    fullDescription = models.TextField(blank=True, null=True, verbose_name="Полное описание")
    freeDelivery = models.BooleanField(default=False, verbose_name="Бесплатная доставка")
    limited = models.BooleanField(default=False, verbose_name="Ограниченный тираж")
    images = models.ManyToManyField(Image, related_name="products", verbose_name="фотографии")
    tags = models.ManyToManyField(Tag, related_name="products", verbose_name="тэги")
    specifications = models.ManyToManyField(Specification, related_name="products", verbose_name="характеристики")
    rating = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Рейтинг")
    on_banner = models.BooleanField(default=False, verbose_name="На баннере")

    @classmethod
    def get_category_items(cls, category_id: int):
        if category_id != -1:
            return Product.objects.filter(category=category_id)
        else:
            return Product.objects.all()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Review(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, related_name="author", verbose_name='Автор'
    )
    text = models.TextField(verbose_name="Отзыв")
    rate = models.PositiveIntegerField(verbose_name="Оценка")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name='Товар')

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class SaleItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales", verbose_name='Товар')
    salePrice = models.FloatField(verbose_name="Цена со скидкой")
    dateFrom = models.DateField(verbose_name="Начало акции")
    dateTo = models.DateField(verbose_name="Конец акции")

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
