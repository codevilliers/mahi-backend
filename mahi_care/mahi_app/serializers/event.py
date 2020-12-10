from rest_framework import serializers

from mahi_app.models import Activity, Suggestion, Donation
from mahi_app.serializers.user import UserProfileSerializer, \
    VolunteerProfileSerializer
from mahi_app.serializers.media import MediaSerializer


class ActivitySerializer(serializers.ModelSerializer):
    person = VolunteerProfileSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = '__all__'


class SuggestionSerializer(serializers.ModelSerializer):
    person = UserProfileSerializer(read_only=True)

    class Meta:
        model = Suggestion
        fields = '__all__'


class DonationSerializer(serializers.ModelSerializer):
    person = UserProfileSerializer(read_only=True)

    class Meta:
        model = Donation
        fields = '__all__'
