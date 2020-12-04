from rest_framework import generics, viewsets
from mahi_app.models import Tags
from rest_framework.response import Response
from rest_framework.views import APIView
from mahi_app.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Tags.objects.all()
    serializer_class = TagSerializer
