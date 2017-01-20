import json

import requests

from django.core import mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.db.models import Q

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
from device.serializers import RoomSerializer
from device.serializers import PlacementSerializer
from device.serializers import DeviceListShortSerializer
from device.serializers import DeviceStateListSerializer

from device.models import Device
from device.models import Room
from device.models import Placement
from device.models import DeviceGroup
from node.models import RequestLog
from button.models import Button

from device.command import Command


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name', 'id',)
    ordering = ('name',)


class DeviceDetailedView(generics.RetrieveAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceDetailSerializer


class DeviceListShortView(APIView):
    serializer_class = DeviceListShortSerializer

    def get(self, request, *args, **kwargs):
        serializer = DeviceListShortSerializer(
            Device.objects.all(), many=True
        )
        return Response(
            serializer.data
        )


class DeviceStatesView(APIView):
    serializer_class = DeviceStateListSerializer

    def get(self, request, *args, **kwargs):
        return Response(
            self.serializer_class(
                Device.objects.all().values('id', 'state'), many=True
            ).data
        )


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
    only_devices_with_state = None
    model = DeviceGroup

    @property
    def entity(self):
        return self.__entity

    def set_model(self, pk):
        try:
            self.__entity = self.model.objects.get(pk=pk)
            return True
        except self.model.DoesNotExist:
            return False

    def execute_command(self, device):
        raise NotImplementedError()


class DeviceCollectionCommandViewOnBase(DeviceCollectionCommandViewBase):
    def execute_request(self, request, **kwargs):
        command = Command(only_devices_with_state=0)
        command.set_location_instance(
            self.entity
        )
        return Response(
            command.turn_on()
        )


class DeviceCollectionCommandViewOffBase(DeviceCollectionCommandViewBase):
    def execute_request(self, request, **kwargs):
        command = Command(only_devices_with_state=1)
        command.set_location_instance(
            self.entity
        )
        return Response(
            command.turn_off()
        )


class DeviceCommandOnView(DeviceCommandViewBase):
    def execute_request(self, request, **kwargs):
        command = Command()
        command.set_location_instance(self.device)
        command.turn_on()
        return Response()


class DeviceCommandOffView(DeviceCommandViewBase):
    def execute_request(self, request, **kwargs):
        command = Command()
        command.set_location_instance(self.device)
        command.turn_off()
        return Response()


class DeviceCommandDimView(DeviceCommandViewBase):
    def execute_request(self, request, **kwargs):
        communicator = self.device.get_communicator()
        if communicator.dim(dimlevel=int(kwargs.get('dimlevel', 0))):
            return Response()


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


class DeviceCategoryViewSetBase(viewsets.ModelViewSet):
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name', 'id',)
    ordering = ('name',)

# Device group collection
class DeviceGroupCommandOnView(DeviceCollectionCommandViewOnBase):
    only_devices_with_state = 0


class DeviceGroupCommandOffView(DeviceCollectionCommandViewOffBase):
    only_devices_with_state = 1


# Rooms
class RoomViewSet(DeviceCategoryViewSetBase):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomCommandOnView(DeviceCollectionCommandViewOnBase):
    only_devices_with_state = 0


class RoomCommandOffView(DeviceCollectionCommandViewOffBase):
    only_devices_with_state = 1

# Placements
class PlacementViewSet(DeviceCategoryViewSetBase):
    queryset = Placement.objects.all()
    serializer_class = PlacementSerializer

class PlacementCommandOnView(DeviceCollectionCommandViewOnBase):
    only_devices_with_state = 0


class PlacementCommandOffView(DeviceCollectionCommandViewOffBase):
    only_devices_with_state = 1
