from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductForm
from .models import Product


def home(request):
	products = Product.objects.filter(is_available=True)
	return render(request, 'app/home.html', {'products': products})


def product_list(request):
	products = Product.objects.all()
	if not request.user.is_authenticated:
		products = products.filter(is_available=True)
	return render(request, 'app/product_list.html', {'products': products})


def product_detail(request, pk):
	product = get_object_or_404(Product, pk=pk)
	if not product.is_available and not request.user.is_authenticated:
		return redirect('product_list')
	return render(request, 'app/product_detail.html', {'product': product})


@login_required
def product_create(request):
	form = ProductForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		product = form.save()
		messages.success(request, f'{product.name} foi adicionado ao cardápio.')
		return redirect('product_detail', pk=product.pk)
	return render(request, 'app/product_form.html', {'form': form, 'page_title': 'Novo produto'})


@login_required
def product_update(request, pk):
	product = get_object_or_404(Product, pk=pk)
	form = ProductForm(request.POST or None, instance=product)
	if request.method == 'POST' and form.is_valid():
		product = form.save()
		messages.success(request, f'{product.name} foi atualizado.')
		return redirect('product_detail', pk=product.pk)
	return render(request, 'app/product_form.html', {'form': form, 'product': product, 'page_title': 'Editar produto'})


@login_required
def product_delete(request, pk):
	product = get_object_or_404(Product, pk=pk)
	if request.method == 'POST':
		name = product.name
		product.delete()
		messages.success(request, f'{name} foi removido do cardápio.')
		return redirect('product_list')
	return render(request, 'app/product_confirm_delete.html', {'product': product})
