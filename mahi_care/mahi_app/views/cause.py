from rest_framework import generics, viewsets
from mahi_app.models import Cause
from rest_framework.response import Response
from rest_framework.views import APIView
from mahi_app.serializers import CauseSerializer


class CauseViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Cause.objects.all()
    serializer_class = CauseSerializer

    def get_queryset(self):
        tag = self.request.query_params.get('tag')
        if tag and int(tag)!=0:
            queryset = Cause.objects.filter(tag=tag)
            return queryset
        else:
            return super().get_queryset()
