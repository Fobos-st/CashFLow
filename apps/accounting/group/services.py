from django.db import transaction
from decimal import Decimal

from .models import GroupAbstractAccount, GroupTransaction
from ...accounts.models import CustomUser


class TransferService:
    @staticmethod
    @transaction.atomic
    def create_transfer(account_id: int, transaction_form, amount: float, user:CustomUser):
        """
        Атомарный метод по созданию транзакции в БД и изменение баланса счета

        Атрибуты:
            account_id (int): id счета
            transaction_form (TransactionForm): Заполненная форма валидным данными
            amount (float): Сумма транзакции
            user: Пользователь производивший создание транзакции
            transaction_account (PersonalTransaction): Экземпляр класса транзакции
            account (PersonalAccount): Экземпляр класс счета

        """
        # Блокируем счета для предотвращения race condition
        account = GroupAbstractAccount.objects.select_for_update().get(id=account_id)

        # Создание записи о переводе
        transaction_account = transaction_form.save(commit=False)
        transaction_account.account = account
        transaction_account.user = user

        # Обновление баланса, сохранение транзакции и баланса
        account.balance = account.balance + Decimal(amount)
        account.save()
        transaction_account.save()