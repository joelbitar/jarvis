import json

import requests

from django.core import mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from device.serializers import DeviceSerializer
from device.models import Device
from node.models import RequestLog
from button.models import Button


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceCommandViewBase(APIView):
    __device = None

    @property
    def device(self):
        return self.__device

    def is_in_test_mode(self):
        if hasattr(mail, 'outbox'):
            return True
        else:
            return False

    def command_data(self, **kwargs):
        raise NotImplementedError()

    def on_success(self, **kwargs):
        pass

    def build_url(self):
        return '{node_url}/devices/{device_pk}/execute/'.format(
                node_url=self.device.node.address,
                device_pk=self.device.pk
            )

    def execute_request(self, url, data):
        if self.is_in_test_mode():
            print('In test mode, does not execute request to', url, data)
            return 200, {}

        response_json = {}
        try:
            response = requests.post(
                url,
                json.dumps(data),
                headers={
                    'content-type': 'application/json'
                }
            )
        except requests.ConnectionError:
            return 503, {
                'error': 'connection_error',
                'message': 'Could not connect to node, perhaps not running?',
                'url': url
            }

        return response.status_code, response_json

    def get(self, request, pk, **kwargs):
        try:
            self.__device = Device.objects.get(pk=pk)
        except Device.DoesNotExist:
            return Response(status=404)

        url, data = self.command_data(**kwargs)

        request_log_object = RequestLog(
            url=url,
            request_data=json.dumps(data)
        )
        request_log_object.save()

        status_code, json_response = self.execute_request(
            url, data
        )

        request_log_object.response_status_code = status_code
        request_log_object.response_data = json.dumps(data) 
        request_log_object.response_received = timezone.now()
        request_log_object.save()

        if status_code not in [200]:
            return Response(
                {
                    'node_status_code': status_code,
                    'node_response': json_response
                },
                status=400
            )

        self.on_success(
            **kwargs
        )

        return Response()


class DeviceCommandOnView(DeviceCommandViewBase):
    def command_data(self):
        url = self.build_url()
        data = {
            'command': 'on',
        }
        return url, data

    def on_success(self):
        self.device.state = 1
        self.device.save()


class DeviceCommandOffView(DeviceCommandViewBase):
    def command_data(self):
        url = self.build_url()
        data = {
            'command': 'off',
        }
        return url, data

    def on_success(self):
        self.device.state = 0
        self.device.save()


class DeviceCommandDimView(DeviceCommandViewBase):
    def command_data(self, dimlevel):
        url = self.build_url()
        data = {
            'command': 'dim',
            'data': {
                'dimlevel': dimlevel
            }
        }
        return url, data

    def on_success(self, dimlevel):
        self.device.state = dimlevel
        self.device.save()


class DeviceCommandLearnView(DeviceCommandViewBase):
    def command_data(self):
        url = self.build_url()
        data = {
                'command': 'learn',
        }
        return url, data


class WriteConfigView(APIView):
    def post(self, request):
        pass


class RestartDaemonView(APIView):
    def post(self, request):
        pass


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
