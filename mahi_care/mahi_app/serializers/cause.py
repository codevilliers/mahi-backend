from rest_framework import serializers

from mahi_app.models import Cause
from mahi_app.serializers import TagSerializer
from mahi_app.serializers.media import MediaSerializer, BenchmarkMediaSerializer
from mahi_app.serializers.user import UserProfileSerializer, \
    VolunteerProfileSerializer
from mahi_app.serializers.event import ActivitySerializer, \
    SuggestionSerializer, \
    DonationSerializer


class CauseSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    media_files = MediaSerializer(read_only=True, many=True)
    supporter_count = serializers.ReadOnlyField()

    class Meta:
        model = Cause
        fields = '__all__'


class CauseDetailSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    media_files = MediaSerializer(read_only=True, many=True)
    benchmark_media = BenchmarkMediaSerializer(read_only=True, many=True)
    created_by = UserProfileSerializer(read_only=True)
    supporter_count = serializers.ReadOnlyField()
    associated_volunteers = VolunteerProfileSerializer(
        read_only=True,
        many=True
    )
    cause_donations = DonationSerializer(read_only=True, many=True)
    cause_suggestions = SuggestionSerializer(read_only=True, many=True)
    cause_activities = ActivitySerializer(read_only=True, many=True)

    class Meta:
        model = Cause
        fields = '__all__'


class CauseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cause
        exclude = ['liked_by', 'tag']
