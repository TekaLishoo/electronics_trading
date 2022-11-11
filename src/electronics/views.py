from django.db.models import Avg, DecimalField, F
from rest_framework import mixins, viewsets
from src.electronics.models import NetworkObject, Product
from src.electronics.serializers import (
    NetworkObjectSerializer,
    NetworkObjectUpdateSerializer,
    ProductsSerializer,
)
from src.electronics.filters import NetworkObjectFilter
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter, SearchFilter
from src.electronics.permissions import IsActive


class NetworkObjectsViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Main viewset for objects of network.
    """

    queryset = NetworkObject.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = NetworkObjectFilter
    permission_classes = (IsActive,)

    def get_serializer_class(self):
        if self.action == "update":
            return NetworkObjectUpdateSerializer
        return NetworkObjectSerializer


class NetworkObjectsBigDebtViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Returns objects of network
    with a debt grater then an average debt.
    """

    queryset = NetworkObject.objects.annotate(average_debt=Avg("debt", output_field=DecimalField())).filter(
        debt__gt=F("average_debt"))
    serializer_class = NetworkObjectSerializer
    permission_classes = (IsActive,)


class ProductsViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Main viewset for products.
    """

    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = (IsActive,)
