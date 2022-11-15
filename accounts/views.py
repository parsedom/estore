from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

from django.shortcuts import render, redirect
# import generic views
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

# import models
from accounts.models import Account

from accounts.forms import RegistrationForm
from django.contrib import messages

# import login and authentication
from django.contrib.auth import authenticate, login, logout


# email stuff
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator


class RegisterView(CreateView):

    model = Account
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    # fields = ['first_name', 'last_name', 'username', 'email', 'password']
    success_url = '/accounts/login'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                         password=password)
            user.phone = phone
            user.save()

            # Email verification
            current_site = get_current_site(self.request)
            mail_subject = 'eStore | Verify your account.'
            message = render_to_string('accounts/acc_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'site_name': 'eStore',
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(self.request, 'Account created successfully. Please check your email for verification link.')
            return redirect('/accounts/login?command=verification&email=' + email)


            # return self.form_valid(form)
        else:
            return self.form_invalid(form)
    #
    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        # form.save()
        messages.success(self.request, 'Account created successfully')
        return super().form_valid(form)


class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('store:store')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            # messages.success(request, 'Logged in successfully')
            return redirect('store:store')
        else:
            messages.error(request, 'Username or password is incorrect')
            return redirect('accounts:login')




class LogoutView(TemplateView,LoginRequiredMixin):
    # template_name = 'accounts/login.html'
    # @login_required(login_url='accounts:login')
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been logged out successfully')
        return redirect('accounts:login')


class ProfileView(DetailView):
    model = Account
    template_name = 'accounts/signin.html'
    slug_field = 'username'


def activate_profile(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        messages.success(request, 'Your account has been activated successfully')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('accounts:register')