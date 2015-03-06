__author__ = 'joel'

from rest_framework import serializers
from device.models import Device


class DeviceSerializer(serializers.ModelSerializer):
    protocol_string = serializers.CharField(read_only=True)
    model_string = serializers.CharField(read_only=True)
    is_dimmable = serializers.BooleanField(read_only=True)

    class Meta:
        model = Device
