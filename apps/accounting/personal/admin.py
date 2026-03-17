from django_mptt_admin.admin import DjangoMpttAdmin
from django.contrib import admin
from .models import PersonalCategory, PersonalAbstractAccount, PersonalTransactionStatus, PersonalTransactionType


@admin.register(PersonalCategory)
class CategoryAdmin(DjangoMpttAdmin):
    """
    Админ-панель модели категорий
    """
    pass

admin.site.register(PersonalTransactionStatus)
admin.site.register(PersonalAbstractAccount)
admin.site.register(PersonalTransactionType)
