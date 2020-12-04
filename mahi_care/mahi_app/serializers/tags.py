from rest_framework import serializers
from mahi_app.models import Tags


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'
