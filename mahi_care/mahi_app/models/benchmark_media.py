from django.db import models

from mahi_app.models import Cause


class BenchmarkMedia(models.Model):

    media = models.FileField(
        upload_to='media_files',
        max_length=255,
    )

    cause = models.ForeignKey(
        Cause,
        related_name='benchmark_media',
        on_delete=models.CASCADE
    )

    def __str__(self):
        id = self.id
        return f"Benchmark Media {id}"

    class Meta:
        verbose_name_plural = "Benchmark media"
