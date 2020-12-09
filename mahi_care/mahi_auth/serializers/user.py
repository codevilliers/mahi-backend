from rest_framework import serializers

from mahi_auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'email_verified',
            'firebase_uid',
            'sign_in_provider'
        ]


class WhoAmISerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'email_verified',
            'firebase_uid',
            'display_picture',
            'sign_in_provider'
        ]
