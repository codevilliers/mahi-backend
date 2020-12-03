from django.contrib.auth import logout
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


class Logout(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            "Successfully logged out",
            status=status.HTTP_200_OK
        )
