from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from catalog.models import Game


class Review(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='reviews',
	)
	rating = models.PositiveSmallIntegerField(
		validators=[MinValueValidator(1), MaxValueValidator(5)],
	)
	comment = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']
		constraints = [
			models.UniqueConstraint(fields=['game', 'author'], name='unique_review_per_game_and_author'),
		]

	def clean(self):
		from django.core.exceptions import ValidationError

		if self.game_id and self.author_id and self.game.owner_id == self.author_id:
			raise ValidationError('Owners cannot review their own games.')

	def __str__(self) -> str:
		return f'Review({self.game} by {self.author})'
