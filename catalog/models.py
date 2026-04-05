from django.conf import settings
from django.db import models


class Category(models.Model):
	name = models.CharField(max_length=60, unique=True)

	class Meta:
		ordering = ['name']

	def __str__(self) -> str:
		return self.name


class Game(models.Model):
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='owned_games',
	)
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True)
	min_players = models.PositiveSmallIntegerField(default=1)
	max_players = models.PositiveSmallIntegerField(default=4)
	categories = models.ManyToManyField(Category, blank=True, related_name='games')

	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['title']

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
