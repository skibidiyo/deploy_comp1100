from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import PeerlyUser


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your full name',
            'class': 'form-input',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'studentname@student.uq.edu.au',
            'class': 'form-input',
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a strong password',
            'class': 'form-input',
            'id': 'password1',
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'class': 'form-input',
        })
    )
    terms = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must agree to the Terms of Service and Privacy Policy.'}
    )

    class Meta:
        model = PeerlyUser
        fields = ('full_name', 'email', 'password1', 'password2', 'terms')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='UQ Email Address',
        widget=forms.EmailInput(attrs={
            'placeholder': 'studentname@student.uq.edu.au',
            'class': 'form-input',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-input',
            'id': 'login-password',
        })
    )
    remember_me = forms.BooleanField(required=False)
