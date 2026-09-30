from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'is_available', 'updated_at')
	list_filter = ('category', 'is_available')
	search_fields = ('name', 'description')
	list_editable = ('price', 'is_available')
