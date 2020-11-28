from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        default=None,
        unique=True,
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True,
    )

    display_picture = models.ImageField(
        upload_to='personal_files',
        max_length=255,
        blank=True,
        null=True,
    )

