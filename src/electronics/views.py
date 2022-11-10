from django.db.models import Avg
from django.shortcuts import render
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

    average_debt = NetworkObject.objects.all().aggregate(Avg("debt"))["debt__avg"]
    queryset = NetworkObject.objects.filter(debt__gt=average_debt)
    serializer_class = NetworkObjectSerializer


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
