from django.core.management.base import BaseCommand, CommandError
from time import sleep
from django.utils import timezone

from datetime import timedelta


from forecast.fetcher import ForecastFetcher
from sensor.models import SensorLog, Sensor, SensorHourly, SensorDaily
import random


class CreateMeanValues(object):
    def run(self):
        for sensor in Sensor.objects.all():
            sensor.temperature = 20
            sensor.humidity = 50
            sensor.save()

        SensorLog.objects.all().delete()
        SensorHourly.objects.all().delete()
        SensorDaily.objects.all().delete()

        for sensor in Sensor.objects.all():
            for i in range(48):
                sensor.temperature = sensor.temperature + random.randint(-3, 3)
                sensor.humidity = sensor.temperature + random.randint(-3, 3)
                sensor.save()

                sensor_log = SensorLog.objects.all().order_by('-pk')[0]

                SensorLog.objects.filter(
                    pk=sensor_log.pk
                ).update(
                    created=timezone.now() - timedelta(hours=i)
                )

                sensor_log = SensorLog.objects.all().order_by('-pk')[0]
                sensor_log.save()

                print(sensor, str(sensor_log.created)[:19], str(sensor_log.temperature) + 'c ' + str(sensor_log.humidity) + '%')


class Command(BaseCommand):
    help = 'Creating fake sensor history..'

    def handle(self, *args, **options):
        cmv = CreateMeanValues()
        cmv.run()




