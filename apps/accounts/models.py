from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер пользователя
    С разбиением ответственности методов по принципу единственной ответственности (SRP)

    Методы:
        validate_email: Проводит валидацию email с помощью готового валидатора Django
        validate_user: Проверяет наличие всех атрибутов и корректность почты
        validate_superuser: Удостоверяется что при создании супер пользователя был указан правильно атрибут is_staff
        в случае его отсутствия задаёт его
        create_user: Создание пользователя
        create_superuser: Создание супер пользователя
    """
    def validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Некорректно ведена электронная почта")

    def validate_user(self, first_name, last_name, email, password):
        if not first_name:
            raise ValueError("Отсутствует имя пользователя")
        if not last_name:
            raise ValueError("Отсутствует фамилия пользователя")

        if email:
            email = self.normalize_email(email)
            validate_email(email)
        else:
            raise ValueError("Отсутствует электронная почта пользователя")

        if not password:
            raise ValueError("Отсутствует пароль пользователя")

    def validate_superuser(self, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь права администратора')
        return extra_fields

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        self.validate_user(first_name, last_name, email, password)

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields = self.validate_superuser(**extra_fields)
        user = self.create_user(first_name, last_name, email, password, **extra_fields)
        return user


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя
    """
    first_name = models.CharField(max_length=64, verbose_name="Имя")
    last_name = models.CharField(max_length=64, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Электронная почта", unique=True)
    username = models.CharField(max_length=64, unique=True, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def full_name(self) -> str:
        """Вовзращает полное имя пользователя"""
        return f"{self.first_name} {self.last_name}"

    @property
    def is_superuser(self) -> [bool]:
        """Возвращает статус атрибута is_staff"""
        return self.is_staff

    def __str__(self):
        return self.full_name
