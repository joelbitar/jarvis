__author__ = 'joel'
from optparse import make_option
import json
import asyncio

import requests

import tellcore.telldus as td

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class RawEventHandler(object):
    __send_to_hub = True

    def __init__(self, send_to_hub=True):
        if send_to_hub is False:
            self.__send_to_hub = False

    def __call__(self, raw_command, controller_id, cid):
        if not self.__send_to_hub:
            print('Command received', raw_command)
            return None

        requests.post(
            settings.HUB_URL + '/command/',
            json.dumps({
                'raw': raw_command
            })
        )

        return True


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--dry',
            action='store_true',
            dest='dry',
            default=False,
            help='Only listens and prints, no sending to hub.'),
        )

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        dispatcher = td.AsyncioCallbackDispatcher(loop)

        raw_event = RawEventHandler(send_to_hub=not options['dry'])

        core = td.TelldusCore(callback_dispatcher=dispatcher)
        callbacks = []
        callbacks.append(core.register_raw_device_event(raw_event))

        loop.run_forever()
