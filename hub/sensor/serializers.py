from rest_framework import serializers
from sensor.models import Sensor
from sensor.models import SensorHourly
from sensor.models import SensorDaily
from sensor.models import SensorLog


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor


class SensorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorLog


class SensorDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorDaily


class SensorHourlySerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorHourly

