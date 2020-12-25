from django.contrib.auth import login
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from firebase_admin import auth

from mahi_auth.models import User
from mahi_auth.serializers.user import UserSerializer, WhoAmISerializer
from mahi_auth.views.update import sync_with_firebase


def get_success_response(user):
    user_serializer = WhoAmISerializer(user)
    success_response_data = {
        'user': user_serializer.data
    }
    return Response(data=success_response_data, status=status.HTTP_200_OK)


def check_phone_number_exists(phone_number):
    users = User.objects.filter(phone_number=phone_number)
    if users:
        return True
    else:
        return False


class Login(GenericAPIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        if request.user.is_authenticated:
            response_data = {
                'error': 'You are already logged in.',
            }
            return Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
        data = request.data
        token = data['token']
        decoded_token = auth.verify_id_token(token)
        firebase_uid = decoded_token.get('uid')
        if firebase_uid:
            email = decoded_token.get('email')
            phone_number = decoded_token.get('phone_number')
            firebase_info = decoded_token.get('firebase')
            email_verified = decoded_token.get('email_verified', False)
            sign_in_provider = firebase_info.get('sign_in_provider', 'django')
            if email is None and phone_number is None:
                response_data = {
                    'error': "Couldn't get credentials",
                }
                return Response(
                    data=response_data,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            if email is not None:
                try:
                    request_user = User.objects.get(email=email)
                    if email_verified != request_user.email_verified:
                        request_user.email_verified = email_verified
                        request_user.save()
                    login(request, request_user)
                    return get_success_response(request_user)
                except User.DoesNotExist:
                    pass
            if phone_number is not None:
                try:
                    request_user = User.objects.get(phone_number=phone_number)
                    login(request, request_user)
                    return get_success_response(request_user)
                except User.DoesNotExist:
                    pass

            user_object = {
                'firebase_uid': firebase_uid,
                'email': email,
                'phone_number': phone_number,
                'sign_in_provider': sign_in_provider
            }
            name = decoded_token.get('name')
            if name is not None:
                name_list = name.split()
                first_name = name_list.pop(0)
                last_name = ' '.join(name_list)
                user_object['first_name'] = first_name
                user_object['last_name'] = last_name
            elif sign_in_provider == 'phone':
                name = data.get('name')
                if name:
                    auth.update_user(
                        firebase_uid,
                        display_name=name,
                    )
                    name_list = name.split()
                    first_name = name_list.pop(0)
                    last_name = ' '.join(name_list)
                    user_object['first_name'] = first_name
                    user_object['last_name'] = last_name
                else:
                    user_object['first_name'] = None
                    user_object['last_name'] = None
            else:
                user_object['first_name'] = None
                user_object['last_name'] = None

            user_object['email_verified'] = email_verified

            user_serializer = UserSerializer(data=user_object)
            user_serializer.is_valid(raise_exception=True)
            request_user = User.objects.create(**user_serializer.validated_data)
            request_user.save()
            login(request, request_user)
            return get_success_response(request_user)

        else:
            response_data = {
                'error': "Invalid credentials",
            }
            return Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )


class CheckPhoneNumberExists(GenericAPIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        data = request.data
        phone_number = data['phone_number']
        phone_number_exists = check_phone_number_exists(phone_number)
        response_data = {'phone_number_exists': phone_number_exists}
        return Response(response_data, status=status.HTTP_200_OK)
