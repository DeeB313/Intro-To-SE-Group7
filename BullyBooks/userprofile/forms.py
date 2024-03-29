from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-1 border border-gray-200'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-1 border border-gray-200'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-1 border border-gray-200'}))
