from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mahi_app.views import TagViewSet, CauseViewSet, ActivityViewSet, SuggestionViewSet, DonationViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'causes', CauseViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'donations', DonationViewSet)
router.register(r'suggestions', SuggestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
