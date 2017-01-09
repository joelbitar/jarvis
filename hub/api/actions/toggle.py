from device.models import Room
from device.models import Device
from device.models import Placement
from device.models import DeviceGroup
from device.models import LightType

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

    def get_light_type(self, slug):
        try:
            return LightType.objects.get(
                slug=slug
            )
        except LightType.DoesNotExist:
            return None


    def run(self, properties):
        raise NotImplementedError()


class ActionToggle(ActionBase):
    def run(self, properties):
        parameters = properties.get('parameters')

        command = Command()

        command.set_all_locations(
            parameters.get('location') == "all"
        )

        command.set_location_instance(
            self.get_location(parameters.get('location'))
        )
        command.set_light_type(
            self.get_light_type(parameters.get('light_type'))
        )

        if parameters.get('device_state') == 'on':
            command.turn_on()

        if parameters.get('device_state') == 'off':
            command.turn_off()
