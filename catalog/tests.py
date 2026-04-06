from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Game


User = get_user_model()


class CatalogViewsTests(TestCase):
	def setUp(self):
		self.owner = User.objects.create_user(username='owner', password='StrongPass123!')
		self.other = User.objects.create_user(username='other', password='StrongPass123!')
		self.staff = User.objects.create_user(username='staff', password='StrongPass123!', is_staff=True)

	def test_game_list_renders_and_search_filters(self):
		Game.objects.create(owner=self.owner, title='Catan', description='Trade')
		Game.objects.create(owner=self.owner, title='Chess', description='Classic')

		response = self.client.get(reverse('catalog:game-list'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Catan')
		self.assertContains(response, 'Chess')

		response = self.client.get(reverse('catalog:game-list'), {'q': 'cat'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Catan')
		self.assertNotContains(response, 'Chess')

	def test_game_create_requires_login(self):
		response = self.client.get(reverse('catalog:game-create'))
		self.assertEqual(response.status_code, 302)
		self.assertIn(reverse('accounts:login'), response['Location'])

	def test_game_create_sets_owner(self):
		self.client.login(username='owner', password='StrongPass123!')
		response = self.client.post(
			reverse('catalog:game-create'),
			data={
				'title': 'Azul',
				'description': 'Tiles',
				'min_players': 2,
				'max_players': 4,
			},
		)
		self.assertEqual(response.status_code, 302)
		game = Game.objects.get(title='Azul')
		self.assertEqual(game.owner, self.owner)

	def test_game_update_permissions_owner_or_staff(self):
		game = Game.objects.create(owner=self.owner, title='Uno', description='Cards')

		self.client.login(username='other', password='StrongPass123!')
		response = self.client.get(reverse('catalog:game-update', kwargs={'pk': game.pk}))
		self.assertEqual(response.status_code, 403)
		self.client.logout()

		self.client.login(username='staff', password='StrongPass123!')
		response = self.client.get(reverse('catalog:game-update', kwargs={'pk': game.pk}))
		self.assertEqual(response.status_code, 200)
		self.client.logout()

		self.client.login(username='owner', password='StrongPass123!')
		response = self.client.post(
			reverse('catalog:game-update', kwargs={'pk': game.pk}),
			data={
				'title': 'Uno Updated',
				'description': 'Cards',
				'min_players': 2,
				'max_players': 10,
			},
		)
		self.assertEqual(response.status_code, 302)
		game.refresh_from_db()
		self.assertEqual(game.title, 'Uno Updated')

	def test_game_delete_owner_or_staff(self):
		game = Game.objects.create(owner=self.owner, title='DeleteMe', description='x')

		self.client.login(username='other', password='StrongPass123!')
		response = self.client.post(reverse('catalog:game-delete', kwargs={'pk': game.pk}))
		self.assertEqual(response.status_code, 403)
		self.assertTrue(Game.objects.filter(pk=game.pk).exists())
		self.client.logout()

		self.client.login(username='owner', password='StrongPass123!')
		response = self.client.post(reverse('catalog:game-delete', kwargs={'pk': game.pk}))
		self.assertEqual(response.status_code, 302)
		self.assertFalse(Game.objects.filter(pk=game.pk).exists())

	def test_toggle_favorite_adds_and_removes(self):
		game = Game.objects.create(owner=self.owner, title='FavMe', description='x')

		self.client.login(username='other', password='StrongPass123!')
		url = reverse('catalog:game-favorite', kwargs={'pk': game.pk})
		response = self.client.post(url)
		self.assertEqual(response.status_code, 302)
		game.refresh_from_db()
		self.assertTrue(game.favorited_by.filter(pk=self.other.pk).exists())

		response = self.client.post(url)
		self.assertEqual(response.status_code, 302)
		game.refresh_from_db()
		self.assertFalse(game.favorited_by.filter(pk=self.other.pk).exists())

	def test_category_crud_owner_flow(self):
		self.client.login(username='owner', password='StrongPass123!')
		response = self.client.post(reverse('catalog:category-create'), data={'name': 'Strategy'})
		self.assertEqual(response.status_code, 302)
		category = Category.objects.get(name='Strategy')
		self.assertEqual(category.created_by, self.owner)

		response = self.client.post(reverse('catalog:category-update', kwargs={'pk': category.pk}), data={'name': 'Euro Strategy'})
		self.assertEqual(response.status_code, 302)
		category.refresh_from_db()
		self.assertEqual(category.name, 'Euro Strategy')

		response = self.client.post(reverse('catalog:category-delete', kwargs={'pk': category.pk}))
		self.assertEqual(response.status_code, 302)
		self.assertFalse(Category.objects.filter(pk=category.pk).exists())

	def test_category_update_forbidden_for_non_owner(self):
		category = Category.objects.create(name='Party', created_by=self.owner)
		self.client.login(username='other', password='StrongPass123!')
		response = self.client.get(reverse('catalog:category-update', kwargs={'pk': category.pk}))
		self.assertEqual(response.status_code, 403)
