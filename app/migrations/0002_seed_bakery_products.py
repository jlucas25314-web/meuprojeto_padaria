from decimal import Decimal
from django.db import migrations


PRODUCTS = [
	{
		'name': 'Pão de fermentação natural',
		'description': 'Casca crocante, miolo macio e 24 horas de paciência.',
		'category': 'paes',
		'price': Decimal('22.00'),
		'image_url': 'https://images.unsplash.com/photo-1589367920969-ab8e050bbb04?auto=format&fit=crop&w=900&q=85',
	},
	{
		'name': 'Croissant de manteiga',
		'description': 'Folhado em camadas, feito com manteiga de verdade.',
		'category': 'folhados',
		'price': Decimal('12.00'),
		'image_url': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=900&q=85',
	},
	{
		'name': 'Pão de queijo da casa',
		'description': 'Queijo meia-cura, casquinha dourada, por dentro puxa.',
		'category': 'paes',
		'price': Decimal('8.00'),
		'image_url': 'https://images.unsplash.com/photo-1784217066854-f2d84aa49532?auto=format&fit=crop&w=900&q=85',
	},
	{
		'name': 'Bolo de fubá com goiabada',
		'description': 'Receita de família com café passado na hora.',
		'category': 'doces',
		'price': Decimal('16.00'),
		'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=900&q=85',
	},
	{
		'name': 'Focaccia de alecrim',
		'description': 'Azeite, sal grosso e alecrim fresco do nosso quintal.',
		'category': 'paes',
		'price': Decimal('19.00'),
		'image_url': 'https://images.unsplash.com/photo-1619531040576-f9416740661b?auto=format&fit=crop&w=900&q=85',
	},
	{
		'name': 'Roll de canela',
		'description': 'Massa fofinha, canela perfumada e cobertura cremosa.',
		'category': 'doces',
		'price': Decimal('14.00'),
		'image_url': 'https://images.unsplash.com/photo-1509365465985-25d11c17e812?auto=format&fit=crop&w=900&q=85',
	},
]


def add_initial_products(apps, schema_editor):
	product_model = apps.get_model('app', 'Product')
	product_model.objects.using(schema_editor.connection.alias).bulk_create(
		[product_model(**product) for product in PRODUCTS]
	)


def remove_initial_products(apps, schema_editor):
	product_model = apps.get_model('app', 'Product')
	product_model.objects.using(schema_editor.connection.alias).filter(
		name__in=[product['name'] for product in PRODUCTS]
	).delete()


class Migration(migrations.Migration):
	dependencies = [('app', '0001_initial')]

	operations = [migrations.RunPython(add_initial_products, remove_initial_products)]