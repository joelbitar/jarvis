__author__ = 'joel'
import json
import requests
from django.conf import settings


class RawEventHandler(object):
    __send_to_hub = True

    def __init__(self, send_to_hub=True):
        if send_to_hub is False:
            self.__send_to_hub = False

    def __call__(self, raw_command, controller_id=None, cid=None):
        if not self.__send_to_hub:
            print('NOT sending command:', raw_command)
            return None

        requests.post(
            settings.HUB_URL + '/event/',
            json.dumps({
                'raw': raw_command
            }),
            headers={
                'content-type': 'application/json'
            }
        )

        return True
