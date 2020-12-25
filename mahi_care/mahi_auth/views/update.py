from threading import Timer
from rest_framework.generics import UpdateAPIView, GenericAPIView
from rest_framework import permissions, response, status
from firebase_admin import auth, _auth_utils

from mahi_auth.serializers.user import UserUpdateSerializer, WhoAmISerializer


def sync_with_firebase(user):
    firebase_user = auth.get_user(user.firebase_uid)
    user_data = firebase_user._data
    email_verified = user_data.get('emailVerified', user.email_verified)
    user.email_verified = email_verified
    user.save()


class UpdateUser(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        user = self.request.user
        return user

    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        data = request.data
        sanitized_data = {}
        if user.sign_in_provider != 'phone':
            sanitized_data = {
                'phone_number': data.get('phone_number', user.phone_number)
            }
            try:
                auth.update_user(
                    user.firebase_uid,
                    phone_number=sanitized_data['phone_number']
                )
            except _auth_utils.PhoneNumberAlreadyExistsError:
                response_data = {
                    'error': 'Phone number already exists'
                }
                return response.Response(
                    data=response_data,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            sanitized_data = {
                'email': data.get('email', user.email),
            }
            if user.email == data.get('email'):
                email_verified = user.email_verified
            else:
                email_verified = False
            sanitized_data['email_verified'] = email_verified
            try:
                auth.update_user(
                    user.firebase_uid,
                    email=sanitized_data['email'],
                    email_verified=sanitized_data['email_verified']
                )
            except _auth_utils.EmailAlreadyExistsError:
                response_data = {
                    'error': 'Email already exists'
                }
                return response.Response(
                    data=response_data,
                    status=status.HTTP_400_BAD_REQUEST
                )
        display_picture = data.get('display_picture')
        print(display_picture)
        if display_picture:
            sanitized_data['display_picture'] = display_picture
        serializer = UserUpdateSerializer(
            instance,
            data=sanitized_data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        user_serializer = WhoAmISerializer(user, context={'request': request})

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset,
            # we need to forcibly invalidate the prefetch cache on the
            # instance.
            instance._prefetched_objects_cache = {}

        return response.Response(user_serializer.data)


class SyncWithFirebaseView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        user = request.user
        timer = Timer(120.0, sync_with_firebase, [user, ])
        timer.start()
        response_data = {
            'message': 'Request received'
        }
        return response.Response(data=response_data, status=status.HTTP_200_OK)
