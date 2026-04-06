from django.contrib import admin

from .models import Notification, RentalRequest


@admin.register(RentalRequest)
class RentalRequestAdmin(admin.ModelAdmin):
	list_display = ('game', 'borrower', 'status', 'requested_at')
	list_filter = ('status',)
	search_fields = ('game__title', 'borrower__username', 'game__owner__username')
	ordering = ('-requested_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
	list_display = ('title', 'user', 'rental_request', 'created_at', 'read_at')
	search_fields = ('title', 'user__username', 'rental_request__game__title')
	ordering = ('-created_at',)
