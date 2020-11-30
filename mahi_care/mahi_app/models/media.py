from django.db import models
from django.db.models import Q
from django.contrib.contenttypes import models as contenttypes_models
from django.contrib.contenttypes import fields as contenttypes_fields
from mahi_app.models import Cause, Donation

class Media(models.Model):
    limit = Q(app_label='mahi_app',model='cause') | Q(app_label='mahi_app',model='donation')

    entity_content_type = models.ForeignKey(
        to=contenttypes_models.ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=limit
    )

    entity_object_id = models.PositiveIntegerField()

    associated_to = contenttypes_fields.GenericForeignKey(
        ct_field='entity_content_type',
        fk_field='entity_object_id',
    )
    
    media = models.FileField(
        upload_to='media_files',
        max_length=255,
        blank=True,
        null=True,
    )