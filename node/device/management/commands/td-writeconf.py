__author__ = 'joel'

from django.core.management.base import BaseCommand, CommandError

from device.conf import RestartTelldusDaemon
from device.conf import TellstickConfigWriter

from device.models import Device

class Command(BaseCommand):
    help = 'Restarts daemon'

    def handle(self, *args, **options):
        tellstick_config_writer = TellstickConfigWriter(
            Device.objects.all()
        )
        print('Writing config...')
        tellstick_config_writer.write_config()

        restart_telldus_daemon = RestartTelldusDaemon()
        restart_telldus_daemon.restart()

