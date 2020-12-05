from django.db import models
from mahi_app import constants


class BankDetail(models.Model):
    bank_name = models.CharField(
        max_length=200, choices=constants.BankOptions)

    ifsc_code = models.CharField(
        max_length=50
    )

    account_no = models.CharField(
        max_length=50
    )

    def __str__(self):
        bank_name = self.bank_name
        account_no = self.account_no
        return f"{bank_name} - {account_no}"
