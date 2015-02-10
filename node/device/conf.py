from django.template import Template, Context
from django.template import loader
from django.conf import settings


class DeviceConfig(object):
    __device = None
    def __init__(self, device):
        self.__device = device

    @property
    def device(self):
        return self.__device

    def render_device_conf(self):
        template = loader.get_template('device.conf')

        context = Context(
            {
                'device': self.device
            }
        )

        return template.render(context)


class TellstickConfig(object):
    __devices = []
    def __init__(self, devices):
        self.__devices = devices or []

    @property
    def devices(self):
        return self.__devices

    def render_config(self):
        template = loader.get_template('tellstick.conf')

        context = Context(
            {
                'devices': self.devices,
                'user': settings.TELLSTICK_USER,
                'group': settings.TELLSTICK_GROUP,
                'device_node': settings.TELLSTICK_DEVICE_NODE,
            }
        )

        return template.render(context)