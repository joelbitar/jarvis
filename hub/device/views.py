import json

import requests

from django.core import mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework import filters

from device.serializers import DeviceSerializer
from device.serializers import DeviceDetailSerializer
from device.serializers import DeviceGroupSerializer
from device.models import Device
from device.models import Room
from device.models import Placement
from device.models import DeviceGroup
from node.models import RequestLog
from button.models import Button


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name', 'id',)
    ordering = ('name',)


class DeviceDetailedView(generics.RetrieveAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceDetailSerializer


class CommandViewBase(APIView):
    def is_in_test_mode(self):
        if hasattr(mail, 'outbox'):
            return True
        else:
            return False

    def execute_request(self, request, **kwargs):
        raise NotImplementedError()

    def set_model(self, pk):
        raise NotImplementedError()

    def get(self, request, pk, **kwargs):
        if not self.set_model(pk=pk):
            return Response(status=404)

        ## HERE, change to using communicator
        success = self.execute_request(
            request,
            **kwargs
        )

        if not success:
            return Response(
                status=500
            )

        return Response()


class DeviceCommandViewBase(CommandViewBase):
    __device = None

    @property
    def device(self):
        return self.__device

    def set_model(self, pk):
        try:
            self.__device = Device.objects.get(pk=pk)
            return True
        except Device.DoesNotExist:
            return False


class DeviceCollectionCommandViewBase(DeviceCommandViewBase):
    __entity = None
    model = DeviceGroup

    @property
    def entity(self):
        return self.__entity

    def get_all_devices(self):
        return self.entity.devices.all()

    def set_model(self, pk):
        try:
            self.__entity = self.model.objects.get(pk=pk)
            return True
        except self.model.DoesNotExist:
            return False

    def execute_request(self, request, **kwargs):
        result = []
        for device in self.entity.devices.all():
            result.append(
                {
                    'device_id': device.pk,
                    'result': self.execute_command(device)
                }
            )

        return Response(result)

    def execute_command(self, device):
        raise NotImplementedError()


class DeviceCommandOnView(DeviceCommandViewBase):
    def execute_request(self, request, **kwargs):
        communicator = self.device.get_communicator()
        if communicator.turn_on():
            return Response()


class DeviceCommandOffView(DeviceCommandViewBase):
    def execute_request(self, request, **kwargs):
        communicator = self.device.get_communicator()
        if communicator.turn_off():
            return Response()


class DeviceCommandDimView(DeviceCommandViewBase):
    def execute_request(self, request, **kwargs):
        communicator = self.device.get_communicator()
        if communicator.dim(dimlevel=int(kwargs.get('dimlevel', 0))):
            return Response()


class RoomCommandViewBase(DeviceCollectionCommandViewBase):
    model = Room


class RoomCommandOnView(RoomCommandViewBase):
    def execute_command(self, device):
        return device.get_communicator().turn_on()

class RoomCommandOffView(RoomCommandViewBase):
    def execute_command(self, device):
        return device.get_communicator().turn_off()


class DeviceCommandLearnView(DeviceCommandViewBase):
    permission_classes = (IsAdminUser, )

    def execute_request(self, request, **kwargs):
        communicator = self.device.get_communicator()
        if communicator.learn():
            return Response()


class DeviceOptionsView(APIView):
    def get(self, request):
        protocol_model_options = [
            {
                'protocol' : {
                    'id' : Device.PROTOCOL_ARCHTEC,
                    'name' : 'arctech',
                    'models' : [
                        {
                            'id': Device.MODEL_CODESWITCH,
                            'name': 'Code switch',
                            },
                        {
                            'id': Device.MODEL_BELL,
                            'name': 'Bell',
                            },
                        {
                            'id': Device.MODEL_SELFLEARNING_SWITCH,
                            'name': 'Selflearning switch',
                            },
                        {
                            'id': Device.MODEL_SELFLEARNING_DIMMER,
                            'name': 'Selflearning dimmer',
                            },
                        ]
                },
            }
        ]

        button_types = []
        for id, name in Button.BUTTON_TYPE_CHOICES:
            button_types.append(
                {
                    'id': id,
                    'name': name,
                }
            )

        return Response(
            {
                'protocol_model_options' : protocol_model_options,
                'button_type_options' : button_types
            }
        )


class DeviceGroupViewSet(viewsets.ModelViewSet):
    queryset = DeviceGroup.objects.all()
    serializer_class = DeviceGroupSerializer


class DeviceGroupCommandViewBase(DeviceCollectionCommandViewBase):
    model = DeviceGroup


class DeviceGroupCommandOnView(DeviceGroupCommandViewBase):
    def execute_command(self, device):
        return device.get_communicator().turn_on()


class DeviceGroupCommandOffView(DeviceGroupCommandViewBase):
    def execute_command(self, device):
        return device.get_communicator().turn_off()


class PlacementCommandViewBase(DeviceCollectionCommandViewBase):
    model = Placement


class PlacementCommandOnView(PlacementCommandViewBase):
    def execute_command(self, device):
        return device.get_communicator().turn_on()


class PlacementCommandOffView(PlacementCommandViewBase):
    def execute_command(self, device):
        return device.get_communicator().turn_off()
