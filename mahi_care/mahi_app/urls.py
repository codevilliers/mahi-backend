from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mahi_app.views import TagViewSet, CauseViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'causes', CauseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]