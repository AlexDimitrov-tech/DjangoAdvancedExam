from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
	list_display = ('username', 'email', 'first_name', 'last_name', 'location', 'is_staff')
	search_fields = ('username', 'email', 'first_name', 'last_name', 'location')
	list_filter = ('is_staff', 'is_superuser', 'is_active')
	fieldsets = UserAdmin.fieldsets + (
		('Community profile', {'fields': ('location', 'avatar', 'bio')}),
	)
