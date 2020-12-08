from rest_framework import generics, viewsets
from mahi_app.models import Cause
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from mahi_app.serializers import CauseSerializer
from mahi_app.serializers.cause import CauseDetailSerializer, \
    CauseCreateSerializer


def missingDataErrorResponse(message):
    response_data = {
        'error': message
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class CauseViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Cause.objects.all()
    serializer_class = CauseSerializer

    def get_queryset(self):
        tag = self.request.query_params.get('tag')
        if tag and int(tag) != 0:
            queryset = Cause.objects.filter(tag=tag)
            return queryset
        else:
            return super().get_queryset()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CauseDetailSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        media_files = data.pop('media_files', None)
        benchmark_media = data.pop('benchmark_media', None)
        create_serializer = CauseCreateSerializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        tags = request.POST.getlist('tag')
        if media_files is None or benchmark_media is None:
            message = 'Please upload the media files.'
            return missingDataErrorResponse(message)
        if not tags:
            message = 'Please add a category for the cause'
            return missingDataErrorResponse(message)
        cause = Cause.objects.create(**create_serializer.validated_data)
        for file in media_files:
            cause.media_files.create(media=file)
        for file in benchmark_media:
            cause.benchmark_media.create(media=file)
        cause.tag.set(tags)
        serializer = CauseDetailSerializer(cause)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
