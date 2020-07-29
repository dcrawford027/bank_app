from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as logout_user
from django.contrib.auth import get_user_model

from app.models import Account, AccountType


def index(request):
    return redirect(reverse('users:login'))


class Main(object):
    template = None

    def get(self, request):
        return render(request, self.get_template())

    def get_template(self):
        if self.template is not None:
            return self.template
        raise ImproperlyConfigured('Template not defined.')


class LoginView(Main, View):
    template = 'login.html'

    def post(self, request):
        user = authenticate(
            request,
            username=request.POST['email'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect(reverse('app:index'))
        messages.error(request, 'Invalid credentials')
        return redirect(reverse('users:login'))


class RegisterView(Main, View):
    template = 'register.html'

    def post(self, request):
        errors = get_user_model().objects.validate_register(request.POST)
        if len(errors) > 0:
            for key, error in errors.items():
                messages.error(request, error)
            return redirect(reverse('users:register'))

        user = get_user_model().objects.create_user(
            email=request.POST['email'],
            password=request.POST['password'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            birthday=request.POST['dob']
        )
        Account.objects.create_account(
            owner=user,
            account_type=AccountType.objects.get(id=2)
        )
        login(request, user)
        return redirect('app:index')


def logout(request):
    logout_user(request)
    return redirect(reverse('users:login'))
