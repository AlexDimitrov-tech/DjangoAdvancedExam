from django.contrib import admin

from .models import Category, Game


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_by')
	search_fields = ('name',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
	list_display = ('title', 'owner', 'min_players', 'max_players', 'created_at')
	list_filter = ('categories',)
	search_fields = ('title', 'owner__username', 'description')
