from django_mptt_admin.admin import DjangoMpttAdmin
from django.contrib import admin
from .models import PersonalCategory, PersonalAccount, PersonalTransactionStatus, PersonalTransactionType, PersonalTransaction


@admin.register(PersonalCategory)
class CategoryAdmin(DjangoMpttAdmin):
    """
    Админ-панель модели категорий
    """
    pass

admin.site.register(PersonalTransactionStatus)
admin.site.register(PersonalAccount)
admin.site.register(PersonalTransactionType)
admin.site.register(PersonalTransaction)
