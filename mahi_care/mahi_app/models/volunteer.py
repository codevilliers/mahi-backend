from django.db import models
from mahi_auth.models import User
from mahi_app.models import Cause


class Volunteer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='volunteer'
    )

    cause = models.ManyToManyField(
        Cause,
        related_name="associated_volunteers",
        blank=True
    )

    def __str__(self):
        user = self.user
        return f"Volunteer: {user}"
