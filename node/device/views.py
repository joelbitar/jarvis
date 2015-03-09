from device.models import Device
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from device.serializers import DeviceSerializer
from device.commands import CommandError
from device.conf import TellstickConfigWriter
from device.conf import RestartTelldusDaemon 


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceCommandView(APIView):
    def get(self, request, pk, format=None):
        return Response()

    def post(self, request, pk, format=None):
        command_name = request.data.get('command')
        command_data = request.data.get('data') or {}

        try:
            device = Device.objects.get(pk=pk)
        except Device.DoesNotExist:
            return Response(status=404)

        try:
            device.commands.execute_command(command_name, **command_data)
        except CommandError as command_error:
            return Response(data={'error': str(command_error)}, status=400)

        return Response()


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

