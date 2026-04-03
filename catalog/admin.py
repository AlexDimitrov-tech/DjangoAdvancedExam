from django.contrib import admin

from .models import Category, Game


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	search_fields = ('name',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
	list_display = ('title', 'owner')
	list_filter = ('categories',)
	search_fields = ('title',)
