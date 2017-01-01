__author__ = 'joel'

from django.core.management.base import BaseCommand, CommandError
from action.models import Action


class Command(BaseCommand):
    help = 'Checks if actions should be executed'

    def handle(self, *args, **options):
        pass
