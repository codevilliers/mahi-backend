from django.db import models
from mahi_auth.models import User
from mahi_app.models import Tags, BankDetails
import uuid

class Cause(models.Model):
    person = models.ForeignKey(
        User,
        related_name='needy_person',
        on_delete=models.CASCADE
    )

    sharing_id = models.UUIDField(
        default=uuid.uuid4, editable=False, db_index=True
    )

    description = models.TextField()

    raised = models.IntegerField(
        default=0,
    )

    goal = models.IntegerField()

    supporter_count = models.IntegerField(
        default=0,
    )

    created_on = models.DateTimeField(auto_now_add=True)

    deadline = models.DateTimeField()

    tag = models.ManyToManyField(
        'Tags',
        related_name='associated_tag',
    )

    bankDetail = models.ForeignKey(
        'BankDetails',
        related_name='associated_account',
        null=True,
        on_delete=models.SET_NULL
    )
