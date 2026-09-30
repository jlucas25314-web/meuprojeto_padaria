from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Product


class StyledAuthenticationForm(AuthenticationForm):
	username = forms.CharField(
		label='Usuário',
		widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'username'}),
	)
	password = forms.CharField(
		label='Senha',
		strip=False,
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}),
	)


class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ('name', 'description', 'category', 'price', 'image_url', 'is_available')
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
			'category': forms.Select(attrs={'class': 'form-select'}),
			'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
			'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link direto da foto (não página de receita)'}),
			'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}