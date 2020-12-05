from rest_framework import serializers

from mahi_app.models import Media


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ['id', 'media']
