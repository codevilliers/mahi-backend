from django.db import models


class NeedyPerson(models.Model):

    name = models.CharField(max_length=63)

    phone_number = models.CharField(max_length=15)

    address = models.CharField(max_length=255)

    email = models.EmailField(blank=True, null=True)

    photo = models.ImageField(
        upload_to='media_files/needy_photos',
        max_length=255,
    )

    def __str__(self):
        name = self.name
        id = self.id
        return f"Person {id}: {name}"

    class Meta:
        verbose_name_plural = "Needy people"
