from django.conf import settings
from django.db import models
from django.utils import timezone

from catalog.models import Game


class RentalRequest(models.Model):
	class Status(models.TextChoices):
		PENDING = 'pending', 'Pending'
		APPROVED = 'approved', 'Approved'
		DENIED = 'denied', 'Denied'
		CANCELLED = 'cancelled', 'Cancelled'
		RETURNED = 'returned', 'Returned'

	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='rental_requests')
	borrower = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='rental_requests',
	)
	message = models.CharField(max_length=240, blank=True)
	status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
	requested_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	decided_at = models.DateTimeField(blank=True, null=True)

	class Meta:
		ordering = ['-requested_at']
		constraints = [
			models.UniqueConstraint(
				fields=['game', 'borrower'],
				condition=models.Q(status='pending'),
				name='unique_pending_request_per_game_and_borrower',
			),
		]

	def __str__(self) -> str:
		return f'{self.borrower} → {self.game} ({self.status})'

	def clean(self):
		from django.core.exceptions import ValidationError

		if self.game_id and self.borrower_id and self.game.owner_id == self.borrower_id:
			raise ValidationError('You cannot request your own game.')

	def can_user_manage(self, user) -> bool:
		if not user or not user.is_authenticated:
			return False
		return user == self.borrower or user == self.game.owner or user.is_staff

	def set_status(self, status: str) -> None:
		self.status = status
		self.decided_at = timezone.now()


class Notification(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='notifications',
	)
	rental_request = models.ForeignKey(
		RentalRequest,
		on_delete=models.CASCADE,
		related_name='notifications',
	)
	title = models.CharField(max_length=120)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	read_at = models.DateTimeField(blank=True, null=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self) -> str:
		return f'Notification({self.user} - {self.title})'
