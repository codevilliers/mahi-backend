from rest_framework import serializers

from mahi_auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'first_name', 'last_name']
