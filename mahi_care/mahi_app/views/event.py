from rest_framework import generics, viewsets
from mahi_app.models import Activity, Suggestion, Donation
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from mahi_app.serializers import ActivitySerializer, DonationSerializer, SuggestionSerializer
from mahi_app.models import Volunteer


class ActivityViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        volunteer = Volunteer.objects.get(user=user)
        data['person'] = volunteer.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class DonationViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user_id = request.user.id
        data['person'] = user_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class SuggestionViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user_id = request.user.id
        data['person'] = user_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
