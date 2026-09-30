from django.db import migrations


IMAGE_REPLACEMENTS = {
	'Pão de fermentação natural': (
		'https://images.unsplash.com/photo-1585478259715-876acc5be8eb?auto=format&fit=crop&w=900&q=85',
		'https://images.unsplash.com/photo-1589367920969-ab8e050bbb04?auto=format&fit=crop&w=900&q=85',
	),
	'Pão de queijo da casa': (
		'https://images.unsplash.com/photo-1608198093002-ad4e0054841a?auto=format&fit=crop&w=900&q=85',
		'https://images.unsplash.com/photo-1784217066854-f2d84aa49532?auto=format&fit=crop&w=900&q=85',
	),
}


def replace_images(apps, schema_editor, reverse=False):
	product_model = apps.get_model('app', 'Product')
	database = schema_editor.connection.alias
	for name, (old_url, new_url) in IMAGE_REPLACEMENTS.items():
		if reverse:
			old_url, new_url = new_url, old_url
		product_model.objects.using(database).filter(name=name, image_url=old_url).update(image_url=new_url)


class Migration(migrations.Migration):
	dependencies = [('app', '0003_alter_product_price')]

	operations = [migrations.RunPython(replace_images, lambda apps, schema_editor: replace_images(apps, schema_editor, reverse=True))]