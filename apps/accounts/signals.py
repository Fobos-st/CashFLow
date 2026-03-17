from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounting.personal.models import (PersonalAccount, PersonalTransactionType,
                                             PersonalTransactionStatus, PersonalCategory)
from apps.accounts.models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PersonalAccount.objects.create(user=instance, currency="RUB", name="Первый счёт")
        PersonalTransactionStatus.objects.create(user=instance, title="Бизнес", is_system=True)
        PersonalTransactionStatus.objects.create(user=instance, title="Личное", is_system=True)
        PersonalTransactionStatus.objects.create(user=instance, title="Налог", is_system=True)

        withdrawals = PersonalTransactionType.objects.create(user=instance, title="Списание", is_system=True)
        category = PersonalCategory.objects.create(user=instance, type_transaction=withdrawals, is_system=True, title="Инфраструктура")
        PersonalCategory.objects.create(user=instance, type_transaction=withdrawals, parent=category,
                                        is_system=True, title="VPS")
        PersonalCategory.objects.create(user=instance, type_transaction=withdrawals, parent=category,
                                        is_system=True, title="Proxy")
        category = PersonalCategory.objects.create(user=instance, type_transaction=withdrawals, is_system=True, title="Маркетинг")
        PersonalCategory.objects.create(user=instance, type_transaction=withdrawals, parent=category,
                                        is_system=True, title="Avito")
        PersonalCategory.objects.create(user=instance, type_transaction=withdrawals, parent=category,
                                        is_system=True, title="Farpost")

        addition = PersonalTransactionType.objects.create(user=instance, title="Пополнение", is_system=True)
        category = PersonalCategory.objects.create(user=instance, type_transaction=addition, is_system=True,
                                                   title="Зарплата")
        PersonalCategory.objects.create(user=instance, type_transaction=addition, parent=category,
                                        is_system=True, title="Основная")
        PersonalCategory.objects.create(user=instance, type_transaction=addition, parent=category,
                                        is_system=True, title="Аванс")
