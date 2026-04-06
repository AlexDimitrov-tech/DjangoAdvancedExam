from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Game


User = get_user_model()


class ApiTests(TestCase):
	def setUp(self):
		self.owner = User.objects.create_user(username='owner', password='StrongPass123!')
		self.game = Game.objects.create(owner=self.owner, title='Catan', description='Trade', min_players=3, max_players=4)

	def test_ping_endpoint_ok(self):
		response = self.client.get(reverse('api-ping'))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {'status': 'ok'})

	def test_games_list_anonymous_ok(self):
		response = self.client.get(reverse('api-game-list'))
		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertIsInstance(payload, list)
		self.assertEqual(payload[0]['title'], 'Catan')

	def test_game_detail_includes_owner_username(self):
		response = self.client.get(reverse('api-game-detail', kwargs={'pk': self.game.pk}))
		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertEqual(payload['id'], self.game.pk)
		self.assertEqual(payload['owner_username'], 'owner')
