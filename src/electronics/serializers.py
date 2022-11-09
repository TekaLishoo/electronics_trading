from rest_framework import serializers
from src.electronics.models import NetworkObject


class NetworkObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = NetworkObject
        fields = "__all__"


class NetworkObjectUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = NetworkObject
        fields = "__all__"
        read_only_fields = ("debt", )





