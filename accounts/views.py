from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
# import generic views
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

# import models
from accounts.models import Account

from accounts.forms import RegistrationForm
from django.contrib import messages


class RegisterView(CreateView):
    model = Account
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    # fields = ['first_name', 'last_name', 'username', 'email', 'password']
    success_url = '/accounts/login'

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         username = form.cleaned_data['username']
    #         email = form.cleaned_data['email']
    #         phone = form.cleaned_data['phone']
    #         password = form.cleaned_data['password']
    #         Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
    #                                     phone=phone, password=password)
    #
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    #
    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        # form.save()
        messages.success(self.request, 'Account created successfully')
        return super().form_valid(form)


class LoginView(TemplateView):
    template_name = 'accounts/login.html'


class LogoutView(TemplateView):
    template_name = 'accounts/login.html'
