from django import forms
from apps.accounting.personal.models import PersonalAccount
from apps.accounting.group.models import GroupAbstractAccount


class CreatePersonalAccountForm(forms.ModelForm):
    class Meta:
        model = PersonalAccount
        fields = ['name', 'balance', 'currency']


class CreateGroupAccountForm(forms.ModelForm):
    class Meta:
        model = GroupAbstractAccount
        fields = ['balance', 'currency', 'name']
