from django import forms

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