from rest_framework import viewsets
from sensor.models import Sensor

from sensor.serializers import SensorSerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


