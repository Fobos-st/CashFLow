import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()  # Получаю модель пользователя


class NameValidationMixin:
    """Миксин для валидации имени и фамилии"""
    @staticmethod
    def validate_name(name: str, field_label: str) -> str:
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s]+$', name):
            raise forms.ValidationError(f'{field_label} может содержать только буквы')
        return name.strip().capitalize()


class CustomUserCreationForm(UserCreationForm, NameValidationMixin):
    """Форма регистрации пользователя"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
            'class': 'auth-control',
            'id': 'reg-email',
            'name': 'email',
            'autocomplete': 'email',
            'required': True}), error_messages={'unique': 'Данная почта уже зарегистрирована'})
    first_name = forms.CharField(required=True, max_length=64, min_length=2, widget=forms.TextInput(attrs={
            'class': 'auth-control',
            'id': 'reg-firstname',
            'name': 'first_name',
            'autocomplete': 'given-name',
            'required': True
        }))
    last_name = forms.CharField(required=True, max_length=64, min_length=2, widget=forms.TextInput(attrs={
            'class': 'auth-control',
            'id': 'reg-firstname',
            'name': 'first_name',
            'autocomplete': 'family-name',
            'required': True
        }))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
            'class': 'auth-control',
            'id': 'reg-password',
            'name': 'password1',
            'autocomplete': 'new-password',
            'minlength': '8',
            'required': True
        }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
            'class': 'auth-control',
            'id': 'reg-password2',
            'name': 'password2',
            'autocomplete': 'new-password',
            'minlength': '8',
            'required': True
        }))

    error_messages = {
        'password_mismatch': 'Пароли не совпадают.',
    }

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']


    def clean_first_name(self) -> str:
        """Валидация имени"""
        first_name = self.cleaned_data.get('first_name')
        return self.validate_name(first_name, 'Имя')


    def clean_last_name(self) -> str:
        """Валидация фамилии"""
        last_name = self.cleaned_data.get('last_name')
        return self.validate_name(last_name, 'Фамилия')

    def clean_email(self) -> str:
        """Валидация email с проверкой уникальности"""
        email = self.cleaned_data.get('email', '').lower().strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['unique'])
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = None
        if commit:
            user.save()
        return user


class CustomUserLoginForm(AuthenticationForm):
    """Форма входа в аккаунт"""
    username = forms.EmailField(widget=forms.EmailInput(attrs={
            'class': 'auth-control',
            'id': 'reg-email',
            'name': 'email',
            'autocomplete': 'email',
            'required': True
        }),
        error_messages={
            'required': 'Email обязателен для заполнения',
            'invalid': 'Введите корректный email адрес'
        })
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'auth-control',
            'id': 'reg-password',
            'name': 'password1',
            'autocomplete': 'current-password',
            'minlength': '8',
            'required': True
        }),
        error_messages={'required': 'Пароль обязателен для заполнения'})

    error_messages = {
        'invalid_login':
            "Неверные учётные данные. Проверьте email и пароль.",
        'inactive': "Этот аккаунт неактивен."
    }

    def clean_username(self) -> str:
        """Нормализует email"""
        email = self.cleaned_data.get('username')
        if email:
            return email.lower().strip()
        return email

    def confirm_login_allowed(self, user) -> None:
        super().confirm_login_allowed(user)
