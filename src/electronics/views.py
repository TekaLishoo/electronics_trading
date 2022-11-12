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
from django.http import HttpResponse
from src.electronics.tasks import send_mail_func
from rest_framework.decorators import action


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

    queryset = NetworkObject.objects.filter(is_active=True)
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = NetworkObjectFilter
    permission_classes = (IsActive,)

    def get_queryset(self):
        return NetworkObject.objects.all().prefetch_related("employees").filter(is_active=True, employees__employees=self.request.user)

    def get_serializer_class(self):
        if self.action == "update":
            return NetworkObjectUpdateSerializer
        return NetworkObjectSerializer

    @action(methods=["get"], detail=True)
    def qr_code(self, request, pk=None):
        """
        <api/networkobjects/{pk}/qr_code/>
        Receive a mail with QR code
        with a contacts of particular network object.
        """

        contacts = NetworkObject.objects.filter(id=pk).values_list("mail", flat=True)[0]
        send_mail_func.delay(request.user.email, contacts)
        return HttpResponse(
            "Sent QR Code in Email Successfully...Check your mail please"
        )


class NetworkObjectsBigDebtViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Returns objects of network
    with a debt grater then an average debt.
    """

    queryset = NetworkObject.objects.annotate(
        average_debt=Avg("debt", output_field=DecimalField())
    ).filter(debt__gt=F("average_debt"))
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

    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductsSerializer
    permission_classes = (IsActive,)
