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
            print(raw_command)
            return None

        endpoint_url = settings.HUB_API_URL + 'event/'

        try:
            requests.post(
                endpoint_url,
                json.dumps({
                    'raw': raw_command
                }),
                headers={
                    'content-type': 'application/json'
                }
            )
        except Exception:
            print('COULD NOT send to hub')
            print('... log:')
            print('API url', settings.HUB_API_URL)
            print('Endpoint url:', endpoint_url)
            print('Raw command', raw_command)

        return True
