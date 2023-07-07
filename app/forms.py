from django import forms
from .models import Producto
from django.contrib.auth.forms import UserCreationForm

class ProductForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'


class CustomUserCreationForm(UserCreationForm):
    pass
