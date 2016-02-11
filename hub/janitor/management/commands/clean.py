__author__ = 'joel'

from django.core.management.base import BaseCommand, CommandError

from janitor.janitor import Scruffy


class Command(BaseCommand):
    help = 'Listen incomming events from all nodes'

    def handle(self, *args, **options):
        Scruffy().clean()

