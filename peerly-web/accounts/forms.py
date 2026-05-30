from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import PeerlyUser
from main.models import StudentProfile


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


class EditProfileForm(forms.Form):
    full_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your full name'})
    )
    degree = forms.CharField(
        max_length=255, required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Bachelor of Computer Science'})
    )
    year = forms.ChoiceField(
        choices=[('', 'Select year')] + StudentProfile.YEAR_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    bio = forms.CharField(
        max_length=500, required=False,
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Tell other students a bit about yourself...'})
    )
    interests = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. machine learning, hiking, chess'})
    )
    birthday = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-input', 'type': 'date'})
    )


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
