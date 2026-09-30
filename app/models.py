from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Product(models.Model):
	class Category(models.TextChoices):
		BREADS = 'paes', 'Pães'
		PASTRIES = 'folhados', 'Folhados'
		SAVORY = 'salgados', 'Salgados'
		SWEETS = 'doces', 'Doces'

	name = models.CharField('nome', max_length=120)
	description = models.TextField('descrição')
	category = models.CharField('categoria', max_length=20, choices=Category.choices)
	price = models.DecimalField('preço', max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	image_url = models.URLField(
		'URL da imagem',
		blank=True,
		help_text='Use o link direto da foto, não o endereço de uma página de receita.',
	)
	is_available = models.BooleanField('disponível no cardápio', default=True)
	created_at = models.DateTimeField('criado em', auto_now_add=True)
	updated_at = models.DateTimeField('atualizado em', auto_now=True)

	class Meta:
		ordering = ['category', 'name']
		verbose_name = 'produto'
		verbose_name_plural = 'produtos'

	def __str__(self):
		return self.name

	@property
	def price_cents(self):
		return int(self.price * 100)

	@property
	def price_display(self):
		return format(self.price, '.2f').replace('.', ',')

	@property
	def display_image(self):
		if self.image_url:
			return self.image_url
		if self.category == self.Category.SAVORY:
			return 'https://images.unsplash.com/photo-1641848421532-b27f3819071c?auto=format&fit=crop&w=900&q=85'
		return 'https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=900&q=85'
