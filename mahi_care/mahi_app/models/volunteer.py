from django.db import models
from mahi_auth.models import User
from mahi_app.models import Cause


class Volunteer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    cause = models.ManyToManyField(
        Cause,
        related_name="associated_volunteers"
    )

    def __str__(self):
        user = self.user
        return f"Volunteer: {user}"
