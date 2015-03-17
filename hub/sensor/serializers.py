from rest_framework import serializers
from sensor.models import Sensor
from sensor.models import SensorLog


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor


class SensorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorLog