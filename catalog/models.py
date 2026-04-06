from django.conf import settings
from django.db import models


class Category(models.Model):
	name = models.CharField(max_length=60, unique=True)
	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='created_categories',
	)

	class Meta:
		ordering = ['name']

	def __str__(self) -> str:
		return self.name

	def can_user_manage(self, user) -> bool:
		if not user or not user.is_authenticated:
			return False
		return user.is_staff or self.created_by == user


class Game(models.Model):
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='owned_games',
	)
	favorited_by = models.ManyToManyField(
		settings.AUTH_USER_MODEL,
		blank=True,
		related_name='favorite_games',
	)
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True)
	cover_image = models.ImageField(upload_to='game_covers/', blank=True, null=True)
	min_players = models.PositiveSmallIntegerField(default=1)
	max_players = models.PositiveSmallIntegerField(default=4)
	categories = models.ManyToManyField(Category, blank=True, related_name='games')

	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['title']

	def clean(self):
		from django.core.exceptions import ValidationError

		if self.min_players and self.max_players and self.min_players > self.max_players:
			raise ValidationError({'max_players': 'Max players cannot be lower than min players.'})

	def __str__(self) -> str:
		return self.title

	@property
	def player_range(self) -> str:
		if self.min_players == self.max_players:
			return f'{self.min_players} players'
		return f'{self.min_players} - {self.max_players} players'

	@property
	def short_description(self) -> str:
		text = (self.description or '').strip()
		if not text:
			return 'No description yet.'
		if len(text) <= 120:
			return text
		return f'{text[:117].rstrip()}...'
