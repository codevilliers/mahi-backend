from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions

from mahi_auth.serializers.user import WhoAmISerializer


class WhoAmIView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = WhoAmISerializer

    def get_object(self):
        user = self.request.user
        return user
