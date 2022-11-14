from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Account


class RegistrationForm(forms.ModelForm):
    # add form-control class to all fields
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'password':
                self.fields[field].widget = forms.PasswordInput()
            self.fields[field].widget.attrs['class'] = 'form-control'

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = Account.objects.filter(email=email)
        if r.count():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        r = Account.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return password
