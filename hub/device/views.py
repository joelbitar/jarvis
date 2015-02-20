from device.models import Device
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from device.serializers import DeviceSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceCommandView(APIView):
    def get(self, request, pk, format=None):
        return Response()

    def post(self, request, pk, format=None):
        command_name = request.data.get('command')

        try:
            device = Device.objects.get(pk=pk)
        except Device.DoesNotExist:
            return Response(status=404)

        try:
            self.send_command(command_name)
        except CommandError as command_error:
            return Response(data={'error': str(command_error)}, status=400)

        return Response()

class WriteConfigView(APIView):
    def post(self, request):
        return Response()


class RestartDaemonView(APIView):
    def post(self, request):
        return Response()

