from rest_framework import serializers

from mahi_app.models import Activity, Suggestion, Donation, Volunteer
from mahi_app.serializers.user import UserProfileSerializer, \
    VolunteerProfileSerializer
from mahi_app.serializers.media import MediaSerializer


class ActivitySerializer(serializers.ModelSerializer):
    person = VolunteerProfileSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['person'] = Volunteer.objects.get(user=user)
        return super().create(validated_data)


class SuggestionSerializer(serializers.ModelSerializer):
    person = UserProfileSerializer(read_only=True)

    class Meta:
        model = Suggestion
        fields = '__all__'

    def create(self, validated_data):
        validated_data['person'] = self.context['request'].user
        return super().create(validated_data)


class DonationSerializer(serializers.ModelSerializer):
    person = UserProfileSerializer(read_only=True)

    class Meta:
        model = Donation
        fields = '__all__'

    def create(self, validated_data):
        validated_data['person'] = self.context['request'].user
        return super().create(validated_data)
