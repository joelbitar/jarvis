__author__ = 'joel'

from rest_framework import serializers
from device.models import Device
from device.models import DeviceGroup


class DeviceDetailNodeSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'id': value.pk,
            'name': value.name,
        }

class DeviceGroupShowOnlyWhenSerializer(serializers.NullBooleanField):
    def to_representation(self, value):
        return {
            DeviceGroup.SHOW_ONLY_WHEN_CHOICE_ALWAYS_SHOW : 'always',
            DeviceGroup.SHOW_ONLY_WHEN_CHOICE_ON : True,
            DeviceGroup.SHOW_ONLY_WHEN_CHOICE_OFF : False
        }.get(
            value
        )


class DeviceSerializer(serializers.ModelSerializer):
    protocol_string = serializers.CharField(read_only=True)
    model_string = serializers.CharField(read_only=True)
    is_dimmable = serializers.BooleanField(read_only=True)
    room = DeviceDetailNodeSerializer(read_only=True)
    placement = DeviceDetailNodeSerializer(read_only=True)

    class Meta:
        model = Device


class DeviceDetailSerializer(DeviceSerializer):
    node = DeviceDetailNodeSerializer(read_only=True)
    room = DeviceDetailNodeSerializer(read_only=True)
    placement = DeviceDetailNodeSerializer(read_only=True)


class DeviceGroupDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name',)


class DeviceGroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    devices = DeviceGroupDeviceSerializer(many=True, read_only=True)
    state = serializers.NullBooleanField(read_only=True)
    show_only_when = DeviceGroupShowOnlyWhenSerializer(read_only=True)

    class Meta:
        model = DeviceGroup
