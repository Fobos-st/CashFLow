from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View

from apps.accounts.forms import CustomUserCreationForm, CustomUserLoginForm


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main:index')
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            request.session.set_expiry(1209600)
            return redirect('main:index')
        else:
            form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main:index')
        form = CustomUserLoginForm()
        return render(request, 'login.html', {'form': form})


    def post(self, request):
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            request.session.set_expiry(1209600)
            return redirect('main:index')
        else:
            print(form.errors)
            form = CustomUserLoginForm()
        return render(request, 'login.html', {'form': form})
