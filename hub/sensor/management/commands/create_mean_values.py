from django.core.management.base import BaseCommand, CommandError
from time import sleep
from django.utils import timezone

from datetime import timedelta


from forecast.fetcher import ForecastFetcher
from sensor.models import SensorLog


class CreateMeanValues(object):
    def run(self):
        first_log = SensorLog.objects.all().order_by('pk')[0]

        for i in range(int((timezone.now() - first_log.created).total_seconds() / (60 * 60))):
            log = SensorLog.objects.filter(
                created__gte = timezone.now() - timedelta(hours=i + 2),
                created__lt = timezone.now() - timedelta(hours=i + 1)
            ).order_by('-pk')[0]
            log.save()

            print(str(log.created))
            # Do not overheat the SD card and sleep a couple of seconds every few iterations.
            if i > 0 and  i % 5 == 0:
                sleep(2)



class Command(BaseCommand):
    help = 'Fetch weather..'

    def handle(self, *args, **options):
        cmv = CreateMeanValues()
        cmv.run()




