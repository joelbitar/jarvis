from device.models import Device
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from device.serializers import DeviceSerializer
from device.conf import TellstickConfigWriter
from device.conf import RestartTelldusDaemon


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


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

