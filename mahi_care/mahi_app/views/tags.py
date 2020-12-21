from rest_framework import viewsets

from mahi_app.permissions import ReadOnly
from mahi_app.models import Tag
from mahi_app.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
