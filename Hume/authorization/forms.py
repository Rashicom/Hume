from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Full name'
        })
    )
    mobile_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Mobile number'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'type': 'email',
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    USER_ROLES = [
        ('STUDENTS', 'STUDENTS'),
        ('RESEARCHER', 'RESEARCHER'),
        ('INSTITUTES', 'INSTITUTES'),
    ]
    role = forms.ChoiceField(choices=USER_ROLES, required=True, label="User Role")

    class Meta:
        model = Account
        fields = ['name', 'mobile_number', 'email', 'password', 'role']


class LoginForm(forms.Form):
    mobile_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Mobile number'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )