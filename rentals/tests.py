from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Game

from .models import RentalRequest


User = get_user_model()


class RentalsViewsTests(TestCase):
	def setUp(self):
		self.owner = User.objects.create_user(username='owner', password='StrongPass123!')
		self.borrower = User.objects.create_user(username='borrower', password='StrongPass123!')
		self.stranger = User.objects.create_user(username='stranger', password='StrongPass123!')
		self.game = Game.objects.create(owner=self.owner, title='Catan', description='Trade')

	def test_owner_cannot_create_rental_request(self):
		self.client.login(username='owner', password='StrongPass123!')
		response = self.client.post(
			reverse('rentals:request-create', kwargs={'game_pk': self.game.pk}),
			data={'message': 'pls'},
		)
		self.assertEqual(response.status_code, 403)
		self.assertEqual(RentalRequest.objects.count(), 0)

	@patch('rentals.views.notify_rental_status_change.delay')
	def test_borrower_can_create_rental_request(self, delay_mock):
		self.client.login(username='borrower', password='StrongPass123!')
		response = self.client.post(
			reverse('rentals:request-create', kwargs={'game_pk': self.game.pk}),
			data={'message': 'Can I borrow this?'},
		)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(RentalRequest.objects.count(), 1)
		rental = RentalRequest.objects.get()
		self.assertEqual(rental.borrower, self.borrower)
		self.assertEqual(rental.game, self.game)
		self.assertEqual(rental.status, RentalRequest.Status.PENDING)
		delay_mock.assert_called()

	@patch('rentals.views.notify_rental_status_change.delay')
	def test_borrower_can_cancel_pending_request(self, delay_mock):
		rental = RentalRequest.objects.create(game=self.game, borrower=self.borrower, message='x')
		self.client.login(username='borrower', password='StrongPass123!')
		response = self.client.post(reverse('rentals:request-cancel', kwargs={'pk': rental.pk}), data={})
		self.assertEqual(response.status_code, 302)
		rental.refresh_from_db()
		self.assertEqual(rental.status, RentalRequest.Status.CANCELLED)
		self.assertIsNotNone(rental.decided_at)
		delay_mock.assert_called()

	@patch('rentals.views.notify_rental_status_change.delay')
	def test_owner_can_decide_on_pending_request(self, delay_mock):
		rental = RentalRequest.objects.create(game=self.game, borrower=self.borrower, message='x')
		self.client.login(username='owner', password='StrongPass123!')
		response = self.client.post(
			reverse('rentals:request-decide', kwargs={'pk': rental.pk}),
			data={'decision': RentalRequest.Status.APPROVED},
		)
		self.assertEqual(response.status_code, 302)
		rental.refresh_from_db()
		self.assertEqual(rental.status, RentalRequest.Status.APPROVED)
		self.assertIsNotNone(rental.decided_at)
		delay_mock.assert_called()

	def test_detail_forbidden_for_stranger(self):
		rental = RentalRequest.objects.create(game=self.game, borrower=self.borrower, message='x')
		self.client.login(username='stranger', password='StrongPass123!')
		response = self.client.get(reverse('rentals:request-detail', kwargs={'pk': rental.pk}))
		self.assertEqual(response.status_code, 403)
