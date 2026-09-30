from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Product


class ProductCatalogTests(TestCase):
	def setUp(self):
		self.product = Product.objects.create(
			name='Croissant de manteiga',
			description='Folhado artesanal.',
			category=Product.Category.PASTRIES,
			price='12.00',
		)

	def test_homepage_displays_products_from_database(self):
		response = self.client.get(reverse('home'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Pão de Casa')
		self.assertContains(response, 'Croissant de manteiga')
		self.assertContains(response, 'R$ 12,00')

	def test_product_list_and_detail_are_public(self):
		listing = self.client.get(reverse('product_list'))
		detail = self.client.get(reverse('product_detail', args=[self.product.pk]))

		self.assertContains(listing, self.product.name)
		self.assertContains(detail, self.product.description)

	def test_product_create_requires_authentication(self):
		response = self.client.get(reverse('product_create'))

		self.assertRedirects(response, f'{reverse("login")}?next={reverse("product_create")}')

	def test_edit_and_delete_require_authentication(self):
		for route_name in ('product_update', 'product_delete'):
			with self.subTest(route=route_name):
				response = self.client.get(reverse(route_name, args=[self.product.pk]))
				self.assertEqual(response.status_code, 302)
				self.assertTrue(response.url.startswith(reverse('login')))

	def test_authenticated_user_can_create_and_update_product(self):
		user = get_user_model().objects.create_user(username='equipe', password='senha-forte-123')
		self.client.force_login(user)
		create_response = self.client.post(reverse('product_create'), {
			'name': 'Pão de queijo',
			'description': 'Queijo meia-cura.',
			'category': Product.Category.BREADS,
			'price': '8.00',
			'is_available': 'on',
		})
		created_product = Product.objects.get(name='Pão de queijo')

		self.assertRedirects(create_response, reverse('product_detail', args=[created_product.pk]))
		update_response = self.client.post(reverse('product_update', args=[created_product.pk]), {
			'name': 'Pão de queijo da casa',
			'description': 'Queijo meia-cura.',
			'category': Product.Category.BREADS,
			'price': '9.00',
			'is_available': 'on',
		})

		created_product.refresh_from_db()
		self.assertRedirects(update_response, reverse('product_detail', args=[created_product.pk]))
		self.assertEqual(created_product.name, 'Pão de queijo da casa')
		self.assertEqual(created_product.price, 9)

	def test_authenticated_user_can_add_savory_product_to_catalog(self):
		user = get_user_model().objects.create_user(username='equipe', password='senha-forte-123')
		self.client.force_login(user)
		response = self.client.post(reverse('product_create'), {
			'name': 'Coxinha de frango',
			'description': 'Massa artesanal com recheio de frango.',
			'category': Product.Category.SAVORY,
			'price': '9.50',
			'is_available': 'on',
		})

		savory_product = Product.objects.get(name='Coxinha de frango')
		self.assertEqual(savory_product.category, Product.Category.SAVORY)
		self.assertRedirects(response, reverse('product_detail', args=[savory_product.pk]))
		self.assertContains(self.client.get(reverse('home')), 'Coxinha de frango')
		self.assertContains(self.client.get(reverse('home')), 'Salgados')

	def test_savory_without_photo_uses_savory_image(self):
		savory_product = Product.objects.create(
			name='Empada',
			description='Empada de palmito.',
			category=Product.Category.SAVORY,
			price='7.00',
		)

		self.assertIn('photo-1641848421532-b27f3819071c', savory_product.display_image)

	def test_product_is_deleted_only_after_post(self):
		user = get_user_model().objects.create_user(username='equipe', password='senha-forte-123')
		self.client.force_login(user)
		delete_url = reverse('product_delete', args=[self.product.pk])

		self.assertEqual(self.client.get(delete_url).status_code, 200)
		self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())
		response = self.client.post(delete_url)

		self.assertRedirects(response, reverse('product_list'))
		self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

	def test_negative_price_is_rejected(self):
		user = get_user_model().objects.create_user(username='equipe', password='senha-forte-123')
		self.client.force_login(user)
		response = self.client.post(reverse('product_create'), {
			'name': 'Produto inválido',
			'description': 'Preço abaixo de zero.',
			'category': Product.Category.BREADS,
			'price': '-1.00',
		})

		self.assertEqual(response.status_code, 200)
		self.assertFalse(Product.objects.filter(name='Produto inválido').exists())

	def test_management_actions_are_hidden_from_anonymous_users(self):
		response = self.client.get(reverse('product_list'))

		self.assertNotContains(response, 'Cadastrar produto')
		self.assertNotContains(response, 'Editar')
