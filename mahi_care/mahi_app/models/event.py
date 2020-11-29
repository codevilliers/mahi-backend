from django.db import models
from mahi_auth.models import User
from mahi_app.models import Cause

class Event(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)

    description = models.TextField()

    class Meta:
        abstract=True

class Activity(Event):
    """
    This model refers to activites associated with cause
    """
    person = models.ForeignKey(
        User,
        related_name='activity_person',
        on_delete=models.CASCADE
    )

    cause = models.ForeignKey(
        'Cause',
        related_name = 'activity_cause',
        on_delete=models.CASCADE
    )

class Suggestion(Event):
    """
    This model refers to suggestion associated with cause
    """
    person = models.ForeignKey(
        User,
        related_name='suggestion_person',
        on_delete=models.CASCADE
    )

    cause = models.ForeignKey(
        'Cause',
        related_name = 'suggestion_cause',
        on_delete=models.CASCADE
    )

class Donation(Event):
    """
    This model refers to donation associated with cause
    """
    person = models.ForeignKey(
        User,
        related_name='donation_person',
        on_delete=models.CASCADE
    )
    cause = models.ForeignKey(
        'Cause',
        related_name = 'donation_cause',
        on_delete=models.CASCADE
    )