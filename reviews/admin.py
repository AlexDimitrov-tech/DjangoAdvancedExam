from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ('game', 'author', 'rating', 'created_at')
	list_filter = ('rating',)
	search_fields = ('game__title', 'author__username')
	ordering = ('-created_at',)
