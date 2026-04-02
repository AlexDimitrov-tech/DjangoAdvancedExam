from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
	location = models.CharField(max_length=120, blank=True)
	avatar = models.URLField(blank=True)
	bio = models.TextField(blank=True)
