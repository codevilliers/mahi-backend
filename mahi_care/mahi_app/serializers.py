from rest_framework import serializers
from mahi_app.models import Cause, Tags

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__' 

class CauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cause
        fields = '__all__' 