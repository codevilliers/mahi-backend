from rest_framework import serializers

from mahi_app.models import Media, BenchmarkMedia


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ['id', 'media']


class BenchmarkMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = BenchmarkMedia
        fields = ['id', 'media']
