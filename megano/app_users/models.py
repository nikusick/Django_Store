from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe


class Avatar(models.Model):
    """Модель аватара пользователя"""

    src = models.ImageField(
        upload_to="static/avatars/",
        verbose_name="Ссылка",
    )
    alt = models.CharField(max_length=128, default="Аватар", verbose_name="Описание")

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"


class Profile(models.Model):
    """Модель профиля пользователя"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullName = models.CharField(max_length=128, verbose_name="Полное имя")
    phone = models.PositiveIntegerField(
        blank=True, null=True, unique=True, verbose_name="Номер телефона"
    )
    avatar = models.ForeignKey(
        Avatar,
        null=True,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Аватар",
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.fullName
