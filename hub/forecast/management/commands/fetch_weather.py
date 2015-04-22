from django.core.management.base import BaseCommand, CommandError

from forecast.fetcher import ForecastFetcher

class Command(BaseCommand):
    help = 'Fetch weather..'

    def handle(self, *args, **options):
        fetcher = ForecastFetcher()
        fetcher.create_entries()




