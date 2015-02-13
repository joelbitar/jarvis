__author__ = 'joel'

from django.core.management.base import BaseCommand, CommandError

from device.conf import RestartTelldusDaemon

class Command(BaseCommand):
    help = 'Restarts daemon'

    def handle(self, *args, **options):
        restart_telldus_daemon = RestartTelldusDaemon()
        restart_telldus_daemon.restart()

