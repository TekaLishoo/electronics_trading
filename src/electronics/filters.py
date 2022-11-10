from django_filters import rest_framework as filters
from src.electronics.models import NetworkObject
from src.core.choices import TYPE_OF_PRODUCT


class NetworkObjectFilter(filters.FilterSet):
    product = filters.ChoiceFilter(
        method="get_product", label="Product", choices=TYPE_OF_PRODUCT
    )

    class Meta:
        model = NetworkObject
        fields = [
            "location_country",
            "product",
        ]

    def get_product(self, queryset, name, value):
        if value:
            return (
                queryset.all()
                .prefetch_related("present_products")
                .filter(present_products__products__name=value)
            )
