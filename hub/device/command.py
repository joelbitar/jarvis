from device.models import Device
from device.models import Room
from device.models import Placement
from device.models import DeviceGroup

from django.db.models import Q


class Command(object):
    only_devices_with_state = None
    location_instance = None
    all_locations = False
    light_type = None

    def __init__(self, only_devices_with_state=None):
        self.only_devices_with_state = only_devices_with_state
        self.light_type = None

    def set_all_locations(self, all_locations):
        self.all_locations = all_locations

    def set_location_instance(self, location_instance):
        self.location_instance = location_instance

    def set_light_type(self, light_type):
        self.light_type = light_type

    def turn_on(self):
        result = []

        if isinstance(self.location_instance, Device):
            return {
                'device_id': self.location_instance.pk,
                'result': self.location_instance.get_communicator().turn_on()
            }

        for device in self.get_all_devices():
            result.append(
                {
                    'device_id': device.pk,
                    'result': device.get_communicator().turn_on()
                }
            )

        return result

    def turn_off(self):
        result = []

        if isinstance(self.location_instance, Device):
            return {
                'device_id': self.location_instance.pk,
                'result': self.location_instance.get_communicator().turn_off()
            }

        for device in self.get_all_devices():
            result.append(
                {
                    'device_id': device.pk,
                    'result': device.get_communicator().turn_off()
                }
            )

        return result

    def get_all_devices(self):
        filters = []

        # If the location instance was not set, returning an empty list
        if self.location_instance is None and self.all_locations is False:
            return []

        if self.light_type is not None:
            filters.append(
                Q(light_type__pk=self.light_type.pk)
            )

        if self.only_devices_with_state is not None:
            if self.only_devices_with_state == 0:
                # If device state is 0 find all devices that are off of None
                filters.append(
                    Q(state=None) | Q(state=0)
                )
            else:
                # If device state is 1 find all devices that are on of None
                filters.append(
                    Q(state=None) | Q(state__gte=1)
                )

        if self.all_locations is True:
            return Device.objects.filter(
                *filters
            )

        return self.location_instance.devices.filter(
            *filters
        )
