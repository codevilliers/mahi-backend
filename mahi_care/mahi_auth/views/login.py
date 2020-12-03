from django.contrib.auth import login
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from firebase_admin import auth

from mahi_auth.models import User
from mahi_auth.serializers.user import UserSerializer


def get_success_response(user):
    user_serializer = UserSerializer(user)
    success_response_data = {
        'status': 'Successfully logged in',
        'user': user_serializer.data
    }
    return Response(data=success_response_data, status=status.HTTP_200_OK)


class Login(GenericAPIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        print('inside post **********')
        if request.user.is_authenticated:
            response_data = {
                'error': 'You are already logged in.',
            }
            return Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
        data = request.data
        # print(data)
        token = data['token']
        # print(token)
        decoded_token = auth.verify_id_token(token)
        print('decoded_token')
        print(decoded_token)
        uid = decoded_token['uid']
        print('uid')
        print(uid)
        user = auth.get_user(uid)
        print('user')
        print(user.__dict__)
        user_data = user._data
        email = user_data.get('email')
        phone_number = user_data.get('phoneNumber')
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
            'email': email,
            'phone_number': phone_number
        }
        name = user_data.get('displayName')
        if name is not None:
            name_list = name.split()
            first_name = name_list.pop(0)
            last_name = ' '.join(name_list)
            user_object['first_name'] = first_name
            user_object['last_name'] = last_name
        else:
            user_object['first_name'] = None
            user_object['last_name'] = None

        user_serializer = UserSerializer(data=user_object)
        user_serializer.is_valid(raise_exception=True)
        request_user = User.objects.create(**user_serializer.validated_data)
        request_user.save()
        login(request, request_user)
        return get_success_response(request_user)
