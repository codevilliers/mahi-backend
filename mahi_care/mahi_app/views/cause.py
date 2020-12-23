from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions, status, filters
from django.db.models import Count

from mahi_app.models import Cause
from mahi_auth.models import User
from mahi_app.serializers import CauseSerializer, SuggestionSerializer, \
    ActivitySerializer
from mahi_app.serializers.cause import CauseDetailSerializer, \
    CauseCreateSerializer
from mahi_app.permissions import IsVolunteer
from mahi_app.pagination import SmallResultsSetPagination


def missingDataErrorResponse(message):
    response_data = {
        'error': message
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class CauseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Cause.objects.filter(is_whitelisted=True)
    serializer_class = CauseSerializer

    def get_queryset(self):
        tag = self.request.query_params.get('tag')
        ordering = self.request.query_params.get('ordering')
        pending = self.request.query_params.get('pending')
        try:
            is_volunteer = self.request.user.is_volunteer()
        except AttributeError:
            is_volunteer = False
        if pending == 'true' and is_volunteer:
            queryset = Cause.objects.filter(is_whitelisted=False)
        else:
            queryset = Cause.objects.filter(is_whitelisted=True)
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

    def get_object(self):
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        try:
            is_volunteer = self.request.user.is_volunteer()
        except AttributeError:
            is_volunteer = False

        if is_volunteer:
            queryset = Cause.objects.all()
            obj = get_object_or_404(queryset, **filter_kwargs)
            self.check_object_permissions(self.request, obj)
            return obj
        else:
            queryset = Cause.objects.filter(is_whitelisted=True)
            obj = get_object_or_404(queryset, **filter_kwargs)
            self.check_object_permissions(self.request, obj)
            return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CauseDetailSerializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_name='get_similar_causes',
            url_path='get_similar_causes',
            pagination_class=SmallResultsSetPagination)
    def get_similar_causes(self, request, pk):
        instance = self.get_object()
        queryset = Cause.objects.filter(tag__in=instance.tag.all())\
            .filter(is_whitelisted=True).exclude(id=pk)
        page = self.paginate_queryset(queryset)
        serializer = CauseSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['PATCH'], url_name='update_liked_user',
            url_path='update_liked_user')
    def update_liked_user(self, request, pk):
        user = User.objects.get(id=request.user.id)
        instance = self.get_object()
        if user not in instance.liked_by.all():
            instance.liked_by.add(user)
        else:
            instance.liked_by.remove(user)
        instance.save()
        serializer = CauseDetailSerializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['PATCH'], url_name='volunteer_request',
            url_path='volunteer_request',
            permission_classes=[permissions.IsAuthenticated, ])
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

    @action(detail=True, methods=['PATCH'], url_name='whitelist_cause',
            url_path='whitelist_cause',
            permission_classes=[permissions.IsAuthenticated & IsVolunteer])
    def whitelist_cause(self, request, pk):
        volunteer = request.user.volunteer
        instance = self.get_object()
        instance.is_whitelisted = True
        instance.associated_volunteers.add(volunteer)
        instance.save()
        response_data = {
            'message': 'Cause whitelisted successfully',
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'], url_name='get_more_suggestions',
            url_path='get_more_suggestions',
            permission_classes=[permissions.AllowAny, ])
    def get_more_suggestions(self, request, pk):
        instance = self.get_object()
        suggestions = instance.cause_suggestions.all()[5:]
        suggestions_serializer = SuggestionSerializer(suggestions, many=True)
        return Response(suggestions_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'], url_name='get_more_activities',
            url_path='get_more_activities',
            permission_classes=[permissions.AllowAny, ])
    def get_more_activities(self, request, pk):
        instance = self.get_object()
        activities = instance.cause_activities.all()[3:]
        activities_serializer = ActivitySerializer(activities, many=True)
        return Response(activities_serializer.data, status=status.HTTP_200_OK)

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
