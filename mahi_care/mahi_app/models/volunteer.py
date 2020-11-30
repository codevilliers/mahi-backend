from django.db import models
from mahi_auth.models import User
from mahi_app.models import Cause

class Volunteer(models.Model):
    user = models.ForeignKey(
        User,on_delete=models.CASCADE
    )

    cause = models.ManyToManyField(
        Cause,
        related_name="assocaited_causes"
    )