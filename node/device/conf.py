from subprocess import call
from django.template import Template, Context
from django.template import loader
from django.conf import settings

from device.commands import BaseCommand


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

        return str(template.render(context))


class TellstickConfig(BaseCommand):
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

        return str(template.render(context))


class TellstickConfigWriter(TellstickConfig):
    def write_config(self):
        if(self.is_in_test_mode()):
            # Fake it till you make it!
            self.devices.update(written_to_conf=True)
            return None

        file = open(settings.TELLSTICK_CONFIG_PATH, 'w')
        file.write(self.render_config())

        if len(self.devices) == 0:
            return None

        print(len(self.devices))

        self.devices.update(written_to_conf=True)


class RestartTelldusDaemon(BaseCommand):
    def restart(self):
        if(self.is_in_test_mode()):
            return None

        call(['sudo', settings.TELLSTICK_RESTART_DAEMON_SCRIPT_PATH])


