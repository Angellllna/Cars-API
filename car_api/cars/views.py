from django.shortcuts import render
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Brand, Car, Model_Car
from .serializers import BrandSerializer, CarSerializer, ModelSerializer


class CarFilter(filters.FilterSet):
    model_name = filters.CharFilter(
        field_name="model__model_name", lookup_expr="icontains"
    )
    engine = filters.CharFilter(field_name="engine", lookup_expr="exact")
    fuel_type = filters.CharFilter(field_name="fuel_type", lookup_expr="exact")
    brand_name = filters.CharFilter(field_name="brand__name", lookup_expr="exact")
    year_min = filters.NumberFilter(field_name="model__year", lookup_expr="gte")
    year_max = filters.NumberFilter(field_name="model__year", lookup_expr="lte")
    body_style = filters.CharFilter(field_name="model__body_style", lookup_expr="exact")
    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")
    mileage_min = filters.NumberFilter(field_name="mileage", lookup_expr="gte")
    mileage_max = filters.NumberFilter(field_name="mileage", lookup_expr="lte")
    exterior_color = filters.CharFilter(
        field_name="exterior_color", lookup_expr="exact"
    )
    interior_color = filters.CharFilter(
        field_name="interior_color", lookup_expr="exact"
    )
    transmission = filters.CharFilter(field_name="transmission", lookup_expr="exact")
    is_on_sale = filters.BooleanFilter(field_name="is_on_sale")

    class Meta:
        model = Car
        fields = []


class CarViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter

    def get_queryset(self):
        if self.request.path == "/cars/all/":
            return Car.objects.filter()

        return Car.objects.filter(is_on_sale=True)

    @action(detail=False, methods=["get"], url_path="all")
    def all_cars(self, request):
        return self.list(request)


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "name": ["exact", "icontains"],
        "country": ["exact", "icontains"],
    }


class ModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Model_Car.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "model_name": ["exact", "icontains"],
        "year": ["gte", "lte"],
        "body_style": ["exact"],
    }
