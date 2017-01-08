from device.models import Room
from device.models import Device
from device.models import Placement
from device.models import DeviceGroup

from device.command import Command


class ActionBase(object):
    def get_location(self, slug):
        filters = {
            'slug': slug
        }

        for model in [Room, Placement, DeviceGroup, Device]:
            try:
                return model.objects.get(**filters)
            except model.DoesNotExist:
                pass

    def run(self, properties):
        raise NotImplementedError()


class ActionToggle(ActionBase):
    def run(self, properties):
        parameters = properties.get('parameters')

        location_instance = self.get_location(parameters.get('location'))

        command = Command(location_instance)

        if parameters.get('device_state') == 'on':
            command.turn_on()

        if parameters.get('device_state') == 'off':
            command.turn_off()
