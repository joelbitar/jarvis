from django.db import models

from button.models import Button
from sensor.models import Sensor
from device.models import Device
from device.models import DeviceGroup


class Action(models.Model):
    """
    an action has none or several buttons and sensors
    and a bunch of devices that it can control.
    """
    name = models.CharField(max_length=256)
    trigger_buttons = models.ManyToManyField(Button, through='ActionButton', related_name='actions')
    trigger_sensors = models.ManyToManyField(Sensor, through='ActionSensor', related_name='actions')

    # Gets controlled
    action_devices = models.ManyToManyField(Device)
    action_device_groups = models.ManyToManyField(DeviceGroup)


class ActionUnitBase(models.Model):
    action = models.ForeignKey(Action)

    def run(self, signal):
        raise NotImplementedError()

    class Meta:
        abstract = True


class ActionSensor(ActionUnitBase):
    """
    Sensors like humidity and temperature sensors
    """
    sensor = models.ForeignKey(Sensor)


class ActionButton(ActionUnitBase):
    """
    This can also be motion sensors, door-sensors (and more?)
    """
    COMMAND_FILTER_NONE = 1
    COMMAND_FILTER_ON = 2
    COMMAND_FILTER_OFF = 3
    CONTROLS_CHOICES = (
        (COMMAND_FILTER_NONE, 'No filter, sends all through'),
        (COMMAND_FILTER_ON, 'Only allow ON commands'),
        (COMMAND_FILTER_OFF, 'Only allow OFF commands'),
    )

    button = models.ForeignKey(Button)

    command_filter = models.PositiveSmallIntegerField(choices=CONTROLS_CHOICES, default=COMMAND_FILTER_NONE, help_text="What signals are passed through")

    def execute_method(self, devices, method_key):
        for device in devices:
            communicator = device.get_communicator()
            method = getattr(communicator, {
                Button.METHOD_ON: 'turn_on',
                Button.METHOD_OFF: 'turn_off',
            }.get(method_key))

            method.__call__()

    def is_valid(self, signal, method_key):
        if self.command_filter == self.COMMAND_FILTER_NONE:
            return True

        if self.command_filter == self.COMMAND_FILTER_ON and method_key == Button.METHOD_ON:
            return True

        if self.command_filter == self.COMMAND_FILTER_OFF and method_key == Button.METHOD_OFF:
            return True

        return False

    def run(self, signal):
        button = self.button
        method_key = button.get_method_identifier(
            signal=signal
        )

        if not self.is_valid(signal, method_key):
            return None

        # Get all communicators and run on them.
        self.execute_method(self.action.action_devices.all(), method_key)

        for group in self.action.action_device_groups.all():
            self.execute_method(group.devices.all(), method_key)

        return True




"""
class ActionSensor(ActionUnitBase):
    TRIGGER_COMMAND_ON = 1
    TRIGGER_COMMAND_OFF = 2
    TRIGGER_COMMAND_CHOICES = (
        (TRIGGER_COMMAND_ON, 'On'),
        (TRIGGER_COMMAND_OFF, 'Off'),
    )

    sensor = models.ForeignKey(Sensor)
    trigger_command = models.PositiveSmallIntegerField(choices=TRIGGER_COMMAND_CHOICES)
"""
