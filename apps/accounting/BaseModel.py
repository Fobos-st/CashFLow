from decimal import Decimal

from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from apps.accounts.models import CustomUser


class AbstractAccount(models.Model):
    """
    Абстракная базовая модель которая содержит в себе дефолтные поля и методы для счетов

    Атрибуты
        balance (DecimalField): Баланс счета, дефолт 0.00, 19 макс общие количество цифр, 2 цифры после запятой
        currency (CharField): Валюта счета
    """
    balance = models.DecimalField(
        verbose_name="Баланс",
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00')
    )
    currency = models.CharField(verbose_name="Валюта",max_length=3, default='RUB')  # добавить choices

    class Meta:
        abstract = True


class AbstractTransactionType(models.Model):
    """
    Абстрактная модель типов транзакций

    Атрибуты
        title (CharField): Название
        is_system (booleanField): Является ли автоматически созданным типом транзакции
        user (ForeignKey -> CustomUser): Автор 'типа' трат
    """
    title = models.CharField(max_length=100)
    is_system = models.BooleanField(default=False)  # системные типы
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='custom_transaction_types'
    )

    class Meta:
        order_by = ['name']
        indexes = [
            models.Index(fields=['user']),
        ]
        abstract = True

    def __str__(self):
        if self.is_system:
            return f"Системный: {self.title}"
        return f"Пользовательский: {self.title} ({self.user.username})"


class AbstractTransactionStatus(models.Model):
    """
    Абстрактная модель статусов транзакции

    Атрибуты
        title (CharField): Название статуса
        is_system (booleanField): Является ли автоматически созданным статусом транзакции
        user (ForeignKey -> CustomUser): Автор 'статуса' транзакции
    """
    title = models.CharField(max_length=100)
    is_system = models.BooleanField(default=False)  # системные типы
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='custom_transaction_status'
    )

    class Meta:
        order_by = ['name']
        indexes = [
            models.Index(fields=['user']),
        ]
        abstract = True

    def __str__(self):
        if self.is_system:
            return f"Системный: {self.title}"
        return f"Пользовательский: {self.title} ({self.user.username})"


class AbstractCategory(MPTTModel):
    """
    Абстрактная модель с древовидной структурой категорий транзакций

    Атрибуты
        title (CharField): Название категории
        parent (TreeForeignKey): родительская категория
        is_system (booleanField): Является ли автоматически созданной категорией транзакции
        user (ForeignKey -> CustomUser): Автор 'категории' транзакции
    """
    title = models.CharField(max_length=100)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    is_system = models.BooleanField(default=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='custom_categories'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        indexes = [
            models.Index(fields=['user', 'type_transaction']),
        ]
        abstract = True

    def __str__(self):
        return self.title
