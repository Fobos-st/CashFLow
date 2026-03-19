from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import TransactionCreateForm
from .models import GroupAbstractAccount, GroupTransaction
from .services import TransferService
from ...accounts.models import CustomUser


def redirect_account(request):
    """Главная страница, если пользователь зарегистрирован то перенаправляет на самый первый перс.счет"""
    if request.user.is_authenticated:
        user_account = GroupAbstractAccount.objects.filter(user=request.user).values_list('id', flat=True).first()
        return redirect('main:index_account', account_id=user_account)
    else:
        return redirect('account:register')


class AccoutingView(View, LoginRequiredMixin):
    """
    Представление персонального счета

    Метод get_context: Возвращает контекст, но для POST возвращает постную инфу(Не хватило времени адекватно реализовать)
    """
    def get_context(self, user:CustomUser, account_id:int, request, get_method=True):
        paginator = Paginator(GroupAbstractAccount.objects.filter(account=account_id), 20)
        page_number = request.GET.get('page')
        page_number = page_number
        try:
            transactions = paginator.page(page_number)
        except PageNotAnInteger:
            transactions = paginator.page(1)
            page_number = 1
        except EmptyPage:
            transactions = paginator.page(paginator.num_pages)

        if get_method:
            return {'form': TransactionCreateForm(user=user), 'account': GroupAbstractAccount.objects.get(pk=account_id),
                    'transactions': transactions, 'page_obj': paginator.get_page(page_number)}
        return (TransactionCreateForm(user=user, data=request.POST),
                GroupAbstractAccount.objects.get(pk=account_id),
                transactions, paginator.get_page(page_number))

    def get(self, request, account_id):
        """
        Возвращает страницу счета по account_id
        form = Форма создания новой транзакции на текущий счет
        account = экземпляр PersonalAccount текщего счета
        transaction = queryset истории транзакий счета
        page_obj = Пагинация истории транзакций
        """
        # Добавить защиту от 3 лиц
        return render(request, "personal_account.html", self.get_context(user=request.user,
                                                                                     account_id=account_id,
                                                                                     request=request))

    def post(self, request, account_id):
        """
        form = Заполненая форма новой транзакции на текущий счет
        account = экземпляр PersonalAccount текщего счета
        transaction = queryset истории транзакий счета
        page_obj = Пагинация истории транзакций
        """
        # Добавить защиту от 3 лиц
        form, account, transaction, page_obj = self.get_context(user=request.user, account_id=account_id, request=request, get_method=False)
        if form.is_valid():
            try:
                TransferService.create_transfer(
                    account_id=account_id, transaction_form=form,
                    amount=float(request.POST['amount']), user=request.user)
                return redirect('main:index_account', account_id=account_id)
            except ValueError as e:
                return render(request, 'personal_account.html', {'error': str(e), 'form': form,
                                                                                     "account": account})
        return render(request, 'personal_account.html', {'form': form, "account": account})

    def delete(self, request):
        """Тут должно было быть удаление транзакций"""
