from rest_framework import serializers

from .models import Brand, Car, Model_Car


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name", "country"]


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model_Car
        fields = ["model_name", "year", "body_style"]


class CarSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    model = ModelSerializer(read_only=True)

    class Meta:
        model = Car
        fields = "__all__"
