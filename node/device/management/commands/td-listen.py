__author__ = 'joel'
from optparse import make_option
import asyncio

import tellcore.telldus as td

from django.core.management.base import BaseCommand, CommandError

from device.management.raw_event_handler import RawEventHandler


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--dry',
            action='store_true',
            dest='dry',
            default=False,
            help='Only listens and prints, no sending to hub.'
        ),
    )

    def handle(self, *args, **options):
        if options['dry']:
            print('Listening to events, but will only print them')

        loop = asyncio.get_event_loop()
        dispatcher = td.AsyncioCallbackDispatcher(loop)

        raw_event = RawEventHandler(send_to_hub=not options['dry'])

        core = td.TelldusCore(callback_dispatcher=dispatcher)
        callbacks = []
        callbacks.append(core.register_raw_device_event(raw_event))

        print('Staring to listen...')
        loop.run_forever()
