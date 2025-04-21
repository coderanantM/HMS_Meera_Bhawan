# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('STUDENT', 'Student'),
        ('WARDEN', 'Warden'),
        ('SUPERINTENDENT', 'Superintendent'),
        ('EMS', 'EMS Team'),
    ]
    
    name = forms.CharField(
        max_length=100,
        required=True,
        label="Full Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter your full name"})
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'user_type', 'password1', 'password2']


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"placeholder": "Enter your email"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}))
