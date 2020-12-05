from rest_framework import serializers

from mahi_app.models import NeedyPerson


class NeedyPersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = NeedyPerson
        fields = '__all__'
