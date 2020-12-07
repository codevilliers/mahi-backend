import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from mahi_auth.models import User
from mahi_app.models import Tag, Media
from mahi_app import constants


class Cause(models.Model):
    created_by = models.ForeignKey(
        User,
        related_name='needy_person',
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

    media_files = GenericRelation(
        Media,
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
        related_name='media_cause'
    )

    is_whitelisted = models.BooleanField(default=False)

    needy_name = models.CharField(max_length=63)

    needy_phone_number = models.CharField(max_length=15)

    needy_address = models.CharField(max_length=255)

    needy_email = models.EmailField(blank=True, null=True)

    needy_photo = models.ImageField(
        upload_to='media_files/needy_photos',
        max_length=255,
    )

    bank_name = models.CharField(
        max_length=200,
        choices=constants.BankOptions,
        null=True,
        blank=True
    )

    bank_ifsc_code = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    bank_account_no = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    bank_upi_id = models.CharField(
        max_length=63,
        null=True,
        blank=True
    )

    def supporter_count(self):
        count = self.liked_by.all().count()
        return count

    def __str__(self):
        id = self.id
        created_by_person = self.created_by
        return f"Cause {id} created by {created_by_person}"
