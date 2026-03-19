from django import forms
from django.db.models import Q
from datetime import date
from .models import PersonalTransaction


class TransactionCreateForm(forms.ModelForm):
    """
    Форма для создания записи о транзакции счета

    Честно не ебу что это
    """
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'value': date.today().strftime('%Y-%m-%d')  # Сегодняшняя дата
        }),
        initial=date.today()
    )

    class Meta:
        model = PersonalTransaction
        fields = ['date', 'amount', 'status', 'transaction_type', 'category', 'comment']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Фильтр: системные записи ИЛИ записи текущего пользователя
        # Нейронка сделала, сам не знаю что это за magic c Q
        user_filter = Q(user=self.user)

        if 'transaction_type' in self.fields:
            self.fields['transaction_type'].queryset = self.fields['transaction_type'].queryset.filter(user_filter)

        if 'status' in self.fields:
            self.fields['status'].queryset = self.fields['status'].queryset.filter(user_filter)

        if 'category' in self.fields:
            self.fields['category'].queryset = self.fields['category'].queryset.filter(user_filter)

        # Стилизация
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input-control'})
