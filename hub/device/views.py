import json

import requests

from django.core import mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

from device.serializers import DeviceSerializer
from device.serializers import DeviceGroupSerializer
from device.models import Device
from device.models import DeviceGroup
from node.models import RequestLog
from button.models import Button


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


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


class DeviceGroupCommandViewBase(DeviceCommandViewBase):
    __group = None
    model = DeviceGroup

    @property
    def group(self):
        return self.__group

    def set_model(self, pk):
        try:
            self.__group = DeviceGroup.objects.get(pk=pk)
            return True
        except DeviceGroup.DoesNotExist:
            return False


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


class DeviceGroupCommandOnView(DeviceGroupCommandViewBase):
    def execute_request(self, request, **kwargs):
        result = []
        for device in self.group.devices.all():
            result.append(
                {
                    'device_id': device.pk,
                    'result': device.get_communicator().turn_on()
                }
            )

        return Response(result)


class DeviceGroupCommandOffView(DeviceGroupCommandViewBase):
    def execute_request(self, request, **kwargs):
        result = []
        for device in self.group.devices.all():
            result.append(
                {
                    'device_id': device.pk,
                    'result': device.get_communicator().turn_off()
                }
            )

        return Response(result)