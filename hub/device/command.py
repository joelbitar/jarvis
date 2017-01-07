from device.models import Device
from device.models import Room
from device.models import Placement
from device.models import DeviceGroup

from django.db.models import Q


class Command(object):
    only_devices_with_state = None
    instance = None

    def __init__(self, instance, only_devices_with_state=None):
        self.instance = instance
        self.only_devices_with_state = only_devices_with_state

    def turn_on(self):
        result = []

        if isinstance(self.instance, Device):
            return {
                'device_id' : self.instance.pk,
                'result' : self.instance.get_communicator().turn_on()
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

        if isinstance(self.instance, Device):
            return {
                'device_id' : self.instance.pk,
                'result' : self.instance.get_communicator().turn_off()
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
        # If we have no restrictions on state
        if self.only_devices_with_state is None:
            return self.instance.devices.all()

        if self.only_devices_with_state == 0:
            # If device state is 0 find all devices that are off of None
            return self.instance.devices.filter(
                Q(state=None) | Q(state=0)
            )
        else:
            # If device state is 1 find all devices that are on of None
            return self.instance.devices.filter(
                Q(state=None) | Q(state__gte=1)
            )
