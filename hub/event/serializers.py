__author__ = 'joel'


from rest_framework import serializers


from event.models import Signal
from event.models import Sender
from button.models import Button
from sensor.models import Sensor


class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal


class RecentSignalSenderSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor


class RecentSignalSenderButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Button


class RecentSignalSenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sender

    sensor = RecentSignalSenderSensorSerializer()
    button = RecentSignalSenderButtonSerializer()

    unit_type = serializers.ReadOnlyField(source='get_unit_type_string')
    name = serializers.ReadOnlyField(source='get_unit_name')


class RecentSignalSerializer(SignalSerializer):
    sender = RecentSignalSenderSerializer()
