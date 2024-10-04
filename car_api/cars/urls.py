from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BrandViewSet, CarViewSet, ModelViewSet

router = DefaultRouter()
router.register(r"cars", CarViewSet, basename="car")
# router.register(r"cars/all", CarAllViewSet, basename="car-all")
router.register(r"brands", BrandViewSet)
router.register(r"models", ModelViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
