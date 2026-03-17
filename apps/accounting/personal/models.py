from decimal import Decimal

from django.db import models
from mptt.fields import TreeForeignKey

from apps.accounting.BaseModel import AbstractAccount, AbstractTransactionStatus, AbstractCategory, AbstractTransactionType
from apps.accounts.models import CustomUser


class PersonalAccount(AbstractAccount):
    """
    Персональный счет пользователя

    Атрибуты
        balance (DecimalField): Баланс счета, дефолт 0.00, 15 макс. общие количество цифр, 2 цифры после запятой(Наследуемый)
        currency (CharField): Валюта счета(Наследуемый)
        user (ForeignKey -> CustomUser): Связь счета с пользователем
        name (CharField): Имя счета
    """
    name = models.CharField(max_length=64)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Владелец счета", related_name='owner_account')

    class Meta:
        db_table = 'personal_accounts'

    def __str__(self):
        return f"Счёт {self.user.full_name}"


class PersonalTransactionType(AbstractTransactionType):
    """Типы трат"""
    class Meta:
        db_table = 'personal_transaction_type'


class PersonalTransactionStatus(AbstractTransactionStatus):
    """Статусы трат"""
    class Meta:
        db_table = 'personal_transaction_status'


class PersonalCategory(AbstractCategory):
    """Древовидная структура категорий"""
    type_transaction = models.ForeignKey(PersonalTransactionType, on_delete=models.DO_NOTHING)
    class Meta:
        db_table = 'personal_category'


class PersonalTransaction(models.Model):
    """
    Транзакции персональных счетов

    Атрибуты:
        account (ForeignKey -> PersonalAccount): На каком счету произведена транзакция
        date (DateField): Дата транзакции
        status (ForeignKey -> PersonalTransactionStatus): Статус транзакции
        transaction_type (ForeignKey -> PersonalTransactionType): Тип транзакции
        category (TreeForeignKey -> PersonalCategory): Категория транзакции
        amount (DecimalField): Сумма транзакции
        comment (CharField): Комментарий к транзакции
    """
    account = models.ForeignKey(PersonalAccount, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.ForeignKey(PersonalTransactionStatus, on_delete=models.PROTECT)
    transaction_type = models.ForeignKey(PersonalTransactionType, on_delete=models.PROTECT)
    category = TreeForeignKey(PersonalCategory, on_delete=models.PROTECT)
    amount = models.DecimalField(
        verbose_name="Сумма",
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00')
    )
    comment = models.CharField(max_length=256, verbose_name="Комментарий")

    class Meta:
        db_table = 'personal_transactions'
        ordering = ['date']
        indexes = [
            models.Index(fields=['account']),
        ]

    def __str__(self):
        return f"{self.amount} на {self.account}"
