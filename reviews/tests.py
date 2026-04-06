from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Game

from .models import Review
from .templatetags.review_extras import stars


User = get_user_model()


class ReviewsViewsTests(TestCase):
	def setUp(self):
		self.owner = User.objects.create_user(username='owner', password='StrongPass123!')
		self.author = User.objects.create_user(username='author', password='StrongPass123!')
		self.other = User.objects.create_user(username='other', password='StrongPass123!')
		self.staff = User.objects.create_user(username='staff', password='StrongPass123!', is_staff=True)
		self.game = Game.objects.create(owner=self.owner, title='Catan', description='Trade')

	def test_create_review(self):
		self.client.login(username='author', password='StrongPass123!')
		response = self.client.post(
			reverse('reviews:review-create', kwargs={'game_pk': self.game.pk}),
			data={'rating': 5, 'comment': 'Great'},
		)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Review.objects.count(), 1)
		review = Review.objects.get()
		self.assertEqual(review.author, self.author)
		self.assertEqual(review.game, self.game)
		self.assertEqual(review.rating, 5)

	def test_update_requires_author_or_staff(self):
		review = Review.objects.create(game=self.game, author=self.author, rating=4, comment='Ok')

		self.client.login(username='other', password='StrongPass123!')
		response = self.client.get(reverse('reviews:review-update', kwargs={'pk': review.pk}))
		self.assertEqual(response.status_code, 403)
		self.client.logout()

		self.client.login(username='staff', password='StrongPass123!')
		response = self.client.get(reverse('reviews:review-update', kwargs={'pk': review.pk}))
		self.assertEqual(response.status_code, 200)

	def test_delete_requires_author_or_staff(self):
		review = Review.objects.create(game=self.game, author=self.author, rating=4, comment='Ok')

		self.client.login(username='other', password='StrongPass123!')
		response = self.client.post(reverse('reviews:review-delete', kwargs={'pk': review.pk}))
		self.assertEqual(response.status_code, 403)
		self.assertTrue(Review.objects.filter(pk=review.pk).exists())

	def test_stars_filter_renders_expected_output(self):
		self.assertEqual(stars(3), '★★★☆☆')
		self.assertEqual(stars('5'), '★★★★★')
		self.assertEqual(stars(None), '')

	def test_review_list_and_detail_pages_render(self):
		review = Review.objects.create(game=self.game, author=self.author, rating=4, comment='Solid game night pick')
		response = self.client.get(reverse('reviews:review-list'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Solid game night pick')

		response = self.client.get(reverse('reviews:review-detail', kwargs={'pk': review.pk}))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Catan')

	def test_owner_cannot_review_own_game(self):
		self.client.login(username='owner', password='StrongPass123!')
		response = self.client.post(
			reverse('reviews:review-create', kwargs={'game_pk': self.game.pk}),
			data={'rating': 5, 'comment': 'My own game is great'},
		)
		self.assertEqual(response.status_code, 403)
