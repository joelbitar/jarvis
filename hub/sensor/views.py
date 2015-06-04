from rest_framework import viewsets
from rest_framework import generics
from sensor.models import Sensor
from sensor.models import SensorLog

from rest_framework.response import Response

from sensor.serializers import SensorSerializer
from sensor.serializers import SensorLogSerializer

from authentication.views import AuthenticationViewBaseClass

class SensorViewSet(AuthenticationViewBaseClass, viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorLogView(AuthenticationViewBaseClass, generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        return Response(
            SensorLogSerializer(SensorLog.objects.all(), many=True).data
        )


