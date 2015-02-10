__author__ = 'joel'

from django.core.management.base import BaseCommand, CommandError
from device.models import Device
from device.conf import TellstickConfigWriter


class Command(BaseCommand):
    help = 'Writes tellstick config file to disk'

    def handle(self, *args, **options):
        devices = Device.objects.all()
        #print('Writing config for {device_count} devices'.format(device_count=str(devices.count())))
        print(devices)
        tellstick_config_writer = TellstickConfigWriter(devices=devices)
        tellstick_config_writer.write_config()

