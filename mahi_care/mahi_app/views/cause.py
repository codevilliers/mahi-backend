from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, status, filters
from django.db.models import Count

from mahi_app.models import Cause
from mahi_auth.models import User
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
        ordering = self.request.query_params.get('ordering')
        queryset = Cause.objects.all()
        if tag and int(tag) != 0:
            queryset = queryset.filter(tag=tag)
        if ordering:
            if ordering == '-created_on' or ordering == 'created_on':
                queryset = queryset.order_by(ordering)
                return queryset
            elif ordering == '-supporter_count' or \
                    ordering == 'supporter_count':
                queryset = queryset.annotate(
                    supporter_count=Count('liked_by')).\
                    order_by(ordering, '-created_on')
                return queryset
            return queryset
        else:
            return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CauseDetailSerializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['PATCH'], url_name='update_liked_user',
            url_path='update_liked_user')
    def update_liked_user(self, request, pk):
        user = User.objects.get(id = request.user.id)
        instance = self.get_object()
        if not user in instance.liked_by.all():
            instance.liked_by.add(user)
        else:
            instance.liked_by.remove(user)
        instance.save()
        serializer = CauseDetailSerializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['PATCH'], url_name='volunteer_request',
            url_path='volunteer_request',
            permission_classes=[permissions.IsAuthenticated,])
    def volunteer_request(self, request, pk):
        user = request.user
        instance = self.get_object()
        if user not in instance.volunteer_request.all():
            instance.volunteer_request.add(user)
            instance.save()
            response_data = {'message': 'Request successful'}
        else:
            response_data = {
                'message': 'You have already requested to volunteer'
            }

        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        data = request.data
        media_files = data.pop('media_files', None)
        benchmark_media = data.pop('benchmark_media', None)
        data['created_by'] = request.user.id
        request.data._mutable = False
        create_serializer = CauseCreateSerializer(data=data)
        create_serializer.is_valid(raise_exception=True)
        tags = request.POST.getlist('tag')
        if benchmark_media is None:
            message = 'Please upload benchmark media.'
            return missingDataErrorResponse(message)
        if not tags:
            message = 'Please add a category for the cause'
            return missingDataErrorResponse(message)
        cause = Cause.objects.create(**create_serializer.validated_data)
        if media_files is not None:
            for file in media_files:
                cause.media_files.create(media=file)
        for file in benchmark_media:
            cause.benchmark_media.create(media=file)
        cause.tag.set(tags)
        serializer = CauseDetailSerializer(cause)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
