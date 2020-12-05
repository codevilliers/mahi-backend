from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from mahi_auth.models import User
from mahi_app.models import Cause, Media, Volunteer


class Event(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)

    description = models.TextField()

    class Meta:
        abstract = True


class Activity(Event):
    """
    This model refers to activities associated with cause
    """
    person = models.ForeignKey(
        Volunteer,
        related_name='volunteer_activities',
        on_delete=models.CASCADE
    )

    cause = models.ForeignKey(
        Cause,
        related_name='cause_activities',
        on_delete=models.CASCADE
    )

    def __str__(self):
        id = self.id
        cause = self.cause
        cause_id = cause.id
        person = self.person
        return f"Activity {id} by {person} for cause {cause_id}"

    class Meta:
        verbose_name_plural = "activities"


class Suggestion(Event):
    """
    This model refers to suggestion associated with cause
    """
    person = models.ForeignKey(
        User,
        related_name='person_suggestions',
        on_delete=models.CASCADE
    )

    cause = models.ForeignKey(
        Cause,
        related_name='cause_suggestions',
        on_delete=models.CASCADE
    )

    def __str__(self):
        id = self.id
        cause = self.cause
        cause_id = cause.id
        person = self.person
        return f"Suggestion {id} by person {person} for cause {cause_id}"


class Donation(Event):
    """
    This model refers to donation associated with cause
    """
    person = models.ForeignKey(
        User,
        related_name='person_donations',
        on_delete=models.CASCADE
    )
    cause = models.ForeignKey(
        Cause,
        related_name='cause_donations',
        on_delete=models.CASCADE
    )

    media_files = GenericRelation(
        Media,
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
        related_name='donation_media'
    )

    def __str__(self):
        id = self.id
        cause = self.cause
        cause_id = cause.id
        person = self.person
        return f"Suggestion {id} by person {person} for cause {cause_id}"
