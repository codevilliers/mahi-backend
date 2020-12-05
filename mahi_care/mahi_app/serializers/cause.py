from rest_framework import serializers

from mahi_app.models import Cause
from mahi_app.serializers import TagSerializer
from mahi_app.serializers.media import MediaSerializer, BenchmarkMediaSerializer
from mahi_app.serializers.user import UserProfileSerializer, \
    VolunteerProfileSerializer
from mahi_app.serializers.event import ActivitySerializer, \
    SuggestionSerializer, \
    DonationSerializer
from mahi_app.serializers.bank_detail import BankDetailSerializer
from mahi_app.serializers.needy import NeedyPersonSerializer


class CauseSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    media_files = MediaSerializer(read_only=True, many=True)

    class Meta:
        model = Cause
        fields = '__all__'


class CauseDetailSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    media_files = MediaSerializer(read_only=True, many=True)
    benchmark_media = BenchmarkMediaSerializer(read_only=True, many=True)
    created_by = UserProfileSerializer(read_only=True)
    needy_person = NeedyPersonSerializer(read_only=True)
    supporter_count = serializers.ReadOnlyField()
    bankDetail = BankDetailSerializer(read_only=True)
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
