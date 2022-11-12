from rest_framework import serializers
from src.electronics.models import (
    NetworkObject,
    PresentProducts,
    ObjectEmployees,
    Product,
)
from src.electronics.validators import validate_presentation_date


class NetworkObjectSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    employees = serializers.SerializerMethodField()

    class Meta:
        model = NetworkObject
        fields = "__all__"

    def get_products(self, *args, **kwargs):
        return PresentProducts.objects.filter(object=args[0]).values_list(
            "products__name", flat=True
        )

    def get_employees(self, *args, **kwargs):
        return ObjectEmployees.objects.filter(object=args[0]).values_list(
            "employees__last_name", flat=True
        )


class NetworkObjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkObject
        fields = "__all__"
        read_only_fields = ("debt",)


class ProductsSerializer(serializers.ModelSerializer):
    presented_objects = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {
            "presentation_data": {"validators": [validate_presentation_date]},
        }

    def get_presented_objects(self, *args, **kwargs):
        return (
            PresentProducts.objects.filter(products=args[0])
            .select_related("object")
            .values_list("object__name", flat=True)
        )
