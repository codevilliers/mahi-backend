from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        _('email address'),
        blank=True,
        null=True,
    )

    username = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        default=None,
        unique=True,
    )

    password = models.CharField(
        _('password'),
        max_length=128,
        blank=True,
        null=True,
        default=None,
    )

    phone_number = models.CharField(
        _('phone number'),
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

    def __str__(self):
        username = self.username
        email = self.email
        phone_number = self.phone_number
        if username:
            return username
        if email:
            return email
        if phone_number:
            return phone_number
        return 'Unknown user'
