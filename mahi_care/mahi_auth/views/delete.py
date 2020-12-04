from django.contrib.auth import logout
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from firebase_admin import auth


class Delete(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        logout(request)
        auth.delete_user(user.firebase_uid)
        user.delete()
        return Response(
            "Successfully deleted account",
            status=status.HTTP_200_OK
        )
