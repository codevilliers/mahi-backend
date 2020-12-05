import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from mahi_auth.models import User
from mahi_app.models import Tag, BankDetail, Media, NeedyPerson


class Cause(models.Model):
    created_by = models.ForeignKey(
        User,
        related_name='needy_person',
        on_delete=models.CASCADE
    )

    needy_person = models.OneToOneField(
        NeedyPerson,
        related_name='needy_cause',
        on_delete=models.CASCADE
    )

    cover_photo = models.ImageField(
        upload_to='media_files/cover_photos',
        max_length=255,
    )

    sharing_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )

    description = models.TextField()

    raised = models.IntegerField(
        default=0,
    )

    goal = models.IntegerField()

    liked_by = models.ManyToManyField(
        User,
        related_name='liked_causes',
        blank=True
    )

    created_on = models.DateTimeField(auto_now_add=True)

    deadline = models.DateTimeField()

    tag = models.ManyToManyField(
        'Tag',
        related_name='associated_tag',
    )

    bankDetail = models.ForeignKey(
        BankDetail,
        related_name='associated_account',
        null=True,
        on_delete=models.SET_NULL
    )

    media_files = GenericRelation(
        Media,
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
        related_name='cause_media'
    )

    is_whitelisted = models.BooleanField(default=False)

    def supporter_count(self):
        count = self.liked_by.all().count()
        return count

    def __str__(self):
        id = self.id
        created_by_person = self.created_by
        return f"Cause {id} created by {created_by_person}"
