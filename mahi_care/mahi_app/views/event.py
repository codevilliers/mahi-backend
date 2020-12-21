from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView

from mahi_app.models import Cause, Activity, Suggestion, Donation
from mahi_app.serializers import ActivitySerializer, DonationSerializer, SuggestionSerializer
from mahi_app.models import Volunteer
from mahi_app.permissions import IsVolunteer
from mahi_app.permissions.read_only import ReadOnly, CreateOrReadOnly


def validate_activity(cause, activity_description):
    """
    Searches the activity for special keywords to update the cause/complaint
    and updates the cause.
    :param cause: The cause for which activity has to be created
    :param activity_description: Description for the activity
    :return : Whether the activity is valid or not
    """
    activity_description_list = activity_description.split(' ')
    activity = activity_description_list[0]
    activity_value = activity_description_list[1]
    if activity == 'DTN':
        try:
            activity_value = int(activity_value)
            if activity_value > cause.raised:
                cause.raised = activity_value
                cause.save()
                return True
            else:
                return False
        except ValueError:
            return False
    else:
        return False


class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated & IsVolunteer]
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        data = request.data
        activity_description = data.get('description')
        cause_id = data.get('cause')
        cause = Cause.objects.get(id=cause_id)
        volunteer = request.user.volunteer
        if cause in volunteer.cause.all():
            if activity_description.startswith('#'):
                activity_description = activity_description[1:]
                activity_description_stripped = activity_description.strip()
                is_valid_activity = validate_activity(
                    cause,
                    activity_description_stripped
                )
                if is_valid_activity:
                    request.data['description'] = activity_description_stripped
                    request.data._mutable = False
                    return super().create(request, *args, **kwargs)
                else:
                    error_response = {
                        'error': 'Invalid activity'
                    }
                    return Response(
                        data=error_response,
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return super().create(request, *args, **kwargs)
        else:
            error_response = {
                'error':
                    'You don\'t have permission to add activity to this cause.'
            }
            return Response(
                data=error_response,
                status=status.HTTP_403_FORBIDDEN
            )


class DonationViewSet(viewsets.ModelViewSet):
    permission_classes = [CreateOrReadOnly, ]
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer


class SuggestionViewSet(viewsets.ModelViewSet):
    permission_classes = [CreateOrReadOnly, ]
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer
