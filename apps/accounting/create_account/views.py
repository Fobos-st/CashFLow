from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import CreatePersonalAccountForm, CreateGroupAccountForm


class CreatePersonalAccountView(View, LoginRequiredMixin):
    """Представление создания нового счета"""
    def post(self, request):
        """Создаёт счет персональный или групповой в зависимости от type_account"""
        if request.POST.get('type_account') == "personal":
            form = CreatePersonalAccountForm(data=request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return redirect('main:index_account', account_id=account.pk)
            else:
                return render(request, 'create_add_account.html')
        elif request.POST.get('type_account') == "group":
            form = CreateGroupAccountForm(data=request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.owner = request.user
                account.save()
                # Не хватило времени дописать в целом (Представления, формы и прочую логику с Групповыми чатами)
        return render(request, 'create_add_account.html')
