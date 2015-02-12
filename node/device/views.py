from device.models import Device
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework import renderers
from rest_framework.response import Response
from device.serializers import DeviceSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer