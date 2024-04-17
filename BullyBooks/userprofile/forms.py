from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'w-full p-1 border border-gray-200'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'w-full p-1 border border-gray-200'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full p-1 border border-gray-200'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-1 border border-gray-200'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-1 border border-gray-200'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full p-1 border border-gray-200'}))
    
    CHOICES =(
        (1, 'Buyer'),
        (2, 'Seller'),
    )
    user_type= forms.ChoiceField(label='What are you registering as?', choices=CHOICES, required=False)
