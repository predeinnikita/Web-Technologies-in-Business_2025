from django import forms
from django.forms import ModelForm
from .models import Product

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(help_text="Enter your personal email")
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, help_text="Your password can't be too similar to your other personal information, must contain at least 8 characters, can't be a commonly used password, and can't be entirely numeric.")
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, help_text="Enter the same password as before, for verification.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

