from rest_framework import serializers

from mahi_auth.models import User
from mahi_app.models import Volunteer


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer to serializer name and display picture of a user

    """
    display_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'display_name', 'display_picture']


class VolunteerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer to serializer name and display picture of a volunteer

    """
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Volunteer
        fields = ['user']
