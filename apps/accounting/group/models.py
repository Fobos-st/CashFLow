from django.db import models
from mptt.fields import TreeForeignKey

from apps.accounting.BaseModel import AbstractAccount, AbstractCategory, AbstractTransactionStatus, AbstractTransactionType
from apps.accounts.models import CustomUser


class GroupAbstractAccount(AbstractAccount):
    """
    Групповой счет

    Атрибуты
        balance (DecimalField): Баланс счета, дефолт 0.00, 15 макс. общие количество цифр, 2 цифры после запятой(Наследуемый)
        currency (CharField): Валюта счета(Наследуемый)
        owner (ForeignKey -> CustomUser): Связь счета с создателем
        slug (SlugField): Slug группы
        entry_code (CharField): Код для вступления в группу
    """
    name = models.CharField(max_length=128, default="Групповой счёт")
    owner = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="Создатель счета", related_name='owner_group')
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    entry_code = models.CharField(max_length=16, unique=True, verbose_name="Код входа")

    class Meta:
        db_table = 'group_accounts'

    def __str__(self):
        return f"Счёт {self.owner.full_name}"


class GroupAccountMember(models.Model):
    """
    Список участников групповых счетов

    Атрибуты:
        group (ForeignKey -> GroupAbstractAccount): К какой группе относится пользователь
        user (ForeignKey -> CustomUser): Пользователь
        status (CharField): Статус заявки (Участник) или только отправил запрос
        role (CharField): Роль в группе
    """
    group = models.ForeignKey(GroupAbstractAccount, on_delete=models.CASCADE, verbose_name="Групповой счет")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Участник")
    status = models.CharField(max_length=32, verbose_name="Статус активности")
    role = models.CharField(max_length=32, verbose_name="Роль")

    class Meta:
        db_table = 'group_members'

    def __str__(self):
        return f"Счёт {self.group.title}, участник {self.user.full_name}"


class GroupTransactionType(AbstractTransactionType):
    """Типы трат — общие и пользовательские"""
    group = models.ForeignKey(GroupAbstractAccount, on_delete=models.CASCADE)


class GroupTransactionStatus(AbstractTransactionStatus):
    """Статусы трат — общие и пользовательские"""
    group = models.ForeignKey(GroupAbstractAccount, on_delete=models.CASCADE)


class GroupCategory(AbstractCategory):
    """Древовидная структура категорий трат"""
    type_transaction = models.ForeignKey(GroupTransactionType, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(GroupAbstractAccount, on_delete=models.CASCADE)


class GroupTransaction(models.Model):
    """
    Транзакции группового счета

    Атрибуты:
        group_account (ForeignKey -> PersonalAccount): К какой группе относится транзакция
        initiator (ForeignKey -> CustomUser): Кто добавил транзакцию
        transaction_type (ForeignKey -> PersonalTransactionType): Тип транзакции
        status (ForeignKey -> PersonalTransactionStatus): Статус транзакции
        category (TreeForeignKey -> PersonalCategory): Категория транзакции
        date (DateField): Дата транзакции
        amount (DecimalField): Сумма транзакции
        comment (CharField): Комментарий к транзакции
    """
    group_account = models.ForeignKey(
        GroupAbstractAccount,
        on_delete=models.CASCADE,
    )
    initiator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(GroupTransactionType, on_delete=models.PROTECT)
    status = models.ForeignKey(GroupTransactionStatus, on_delete=models.PROTECT)
    category = TreeForeignKey(GroupCategory, on_delete=models.PROTECT)
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    comment = models.CharField(max_length=256)


    class Meta:
        db_table = 'group_transactions'
        indexes = [
            models.Index(fields=['group_account', 'date']),
            models.Index(fields=['group_account', 'initiator', 'date']),
        ]

    def __str__(self):
        return f"{self.amount} в {self.group_account.title}"
