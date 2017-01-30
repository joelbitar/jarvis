from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from datetime import timedelta


from forecast.fetcher import ForecastFetcher
from sensor.models import SensorLog
from sensor.signals import CreateHourly
from sensor.signals import CreateDaily


class CreateMeanValues(object):
    def run(self):
        pass


class Command(BaseCommand):
    help = 'Fetch weather..'

    def handle(self, *args, **options):
        cmv = CreateMeanValues()
        cmv.run()




