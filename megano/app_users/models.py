from django.contrib.auth.models import User
from django.db import models


class Avatar(models.Model):
    src = models.ImageField(
        upload_to="static/avatars/",
        verbose_name="Ссылка",
    )
    alt = models.CharField(max_length=128, default="Аватар", verbose_name="Описание")

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"

    @classmethod
    def get_default_img(cls):
        return cls._meta.get_field('src').get_default()


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    fullName = models.CharField(max_length=128, verbose_name="Полное имя")
    phone = models.PositiveIntegerField(
        blank=True, null=True, unique=True, verbose_name="Номер телефона"
    )
    balance = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, verbose_name="Баланс"
    )
    avatar = models.ForeignKey(
        Avatar,
        null=True,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Аватар",
    )
