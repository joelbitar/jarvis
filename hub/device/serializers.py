__author__ = 'joel'

from rest_framework import serializers
from device.models import Device
from device.models import DeviceGroup


class DeviceSerializer(serializers.ModelSerializer):
    protocol_string = serializers.CharField(read_only=True)
    model_string = serializers.CharField(read_only=True)
    is_dimmable = serializers.BooleanField(read_only=True)

    class Meta:
        model = Device


class DeviceGroupDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name',)


class DeviceGroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    devices = DeviceGroupDeviceSerializer(many=True, read_only=True)

    class Meta:
        model = DeviceGroup
