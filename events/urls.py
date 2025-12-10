from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EventViewSet, RSVPViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'rsvps', RSVPViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
