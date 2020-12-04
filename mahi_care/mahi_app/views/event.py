from rest_framework import generics, viewsets
from mahi_app.models import Activity, Suggestion, Donation
from rest_framework.response import Response
from rest_framework.views import APIView
from mahi_app.serializers import ActivitySerializer, DonationSerializer, SuggestionSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class DonationViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer


class SuggestionViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer
