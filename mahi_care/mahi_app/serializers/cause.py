from rest_framework import serializers
from mahi_app.models import Cause
from mahi_app.serializers import TagSerializer


class CauseSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Cause
        fields = '__all__'
