__author__ = 'joel'
from optparse import make_option
import json
import asyncio

import requests

import tellcore.telldus as td

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from device.management.raw_event_handler import RawEventHandler


class Command(BaseCommand):
    args = "<events>"
    def handle(self, *args, **options):
        event_handler = RawEventHandler()
        event_handler.connect()

        if len(args) == 0:
            test_args = [
                'class:command;protocol:arctech;model:selflearning;house:2887766;unit:1;group:0;method:turnon;', # from internet.
            ]
            print('Test commands')
            for test_arg in test_args:
                print(test_arg)

            if input('Should we use a bunch of test commands? (printed above) (Y/n)') in [None, 'y', 'Y', '']:
                args = test_args

        for arg in args:
            event_handler(arg)

