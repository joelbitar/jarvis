__author__ = 'joel'

from django.core.management.base import BaseCommand, CommandError

from time import sleep
from device.models import Device
from device.commands import CommandDispatcher
from device.models import DeviceCommand


class Command(BaseCommand):
    help = 'Executes commands..'

    def handle(self, *args, **options):
        while True:
            if not DeviceCommand.objects.filter(executed=None).exists():
                sleep(0.2)
                continue

            for device_command in DeviceCommand.objects.filter(executed=None):
                print('executing...')
                device_command.execute()
