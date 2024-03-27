from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'price', 'image',)
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full p-1 border border-gray-200'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full p-1 border border-gray-200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-1 border border-gray-200'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full p-1 border border-gray-200'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full p-1 border border-gray-200'
            })
            
        }