from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    firebase_uid = models.CharField(
        max_length=150,
        blank=True,
        default=None,
        null=True,
    )

    sign_in_provider = models.CharField(
        max_length=20,
        default='django'
    )

    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=True,
        default=None,
        null=True,
    )

    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True,
        default=None,
        null=True,
    )

    email = models.EmailField(
        _('email address'),
        blank=True,
        null=True,
        default=None,
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
        default=None,
    )

    email_verified = models.BooleanField(default=False)

    display_picture = models.ImageField(
        upload_to='personal_files',
        max_length=255,
        blank=True,
        null=True,
    )

    def display_name(self):
        first_name = self.first_name
        last_name = self.last_name
        return f"{first_name} {last_name}"

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
