from rest_framework import serializers

from mahi_app.models import Cause
from mahi_app.serializers import TagSerializer
from mahi_app.serializers.media import MediaSerializer


class CauseSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    media_files = MediaSerializer(read_only=True, many=True)

    class Meta:
        model = Cause
        fields = '__all__'
