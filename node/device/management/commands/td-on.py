__author__ = 'joel'

from django.core.management.base import BaseCommand, CommandError
from device.models import Device
from device.commands import CommandDispatcher


class Command(BaseCommand):
    args = '<device id>'
    help = 'Turns on a specific device'

    def handle(self, *args, **options):
        device_id = args[0]
        device = Device.objects.get(pk=device_id)
        device.commands.turn_on()
