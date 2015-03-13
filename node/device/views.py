from device.models import Device
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from device.serializers import DeviceSerializer
from device.commands import CommandError
from device.models import DeviceCommand
from device.conf import TellstickConfigWriter
from device.conf import RestartTelldusDaemon
from device.commands import CommandDispatcher

import json


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceCommandView(APIView):
    def get(self, request, pk, format=None):
        return Response()

    # /execute/
    def post(self, request, pk, format=None):
        command_name = request.data.get('command')
        command_data = request.data.get('data') or {}

        try:
            device = Device.objects.get(pk=pk)
        except Device.DoesNotExist:
            return Response(status=404)

        if not device.written_to_conf:
            return Response(
                {
                    'error': 'not-written-to-conf',
                    'message' : 'Device is NOT written to conf, and thus it is not usefull to execute commands on them'
                },
                status=409
            )

        if not command_name in CommandDispatcher.COMMAND_NAME_WHITE_LIST:
            return Response(data={'error': 'command not in list'}, status=400)

        # Create command.
        device_command = DeviceCommand(
            command_name=command_name,
            device=device,
            command_data=command_data
        )
        device_command.save()

        return Response(
            {},
            status=202
        )


class WriteConfigView(APIView):
    def post(self, request):
        tellstick_config_writer = TellstickConfigWriter(devices=Device.objects.all())
        tellstick_config_writer.write_config()

        return Response()


class RestartDaemonView(APIView):
    def post(self, request):
        restart_daemon = RestartTelldusDaemon()
        restart_daemon.restart()

        return Response()

