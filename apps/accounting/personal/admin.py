from django_mptt_admin.admin import DjangoMpttAdmin
from django.contrib import admin
from .models import PersonalCategory


@admin.register(PersonalCategory)
class CategoryAdmin(DjangoMpttAdmin):
    """
    Админ-панель модели категорий
    """
    pass
