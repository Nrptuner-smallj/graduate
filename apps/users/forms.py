from django import forms
from .models import UserProfile


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    nickname = forms.CharField(required=True)
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True)
    code = forms.CharField(required=True, max_length=6)


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
