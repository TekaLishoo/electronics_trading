from django.shortcuts import render
from rest_framework import mixins, viewsets
from src.electronics.models import NetworkObject
from src.electronics.serializers import NetworkObjectSerializer, NetworkObjectUpdateSerializer


class NetworkObjectsViewSet(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet, ):
    queryset = NetworkObject.objects.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return NetworkObjectUpdateSerializer
        return NetworkObjectSerializer
