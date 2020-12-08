from rest_framework import generics, viewsets
from rest_framework.decorators import action
from mahi_app.models import Cause
from mahi_auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from mahi_app.serializers import CauseSerializer
from mahi_app.serializers.cause import CauseDetailSerializer


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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CauseDetailSerializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['PATCH'], url_name='update_liked_user', url_path='update_liked_user')
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
