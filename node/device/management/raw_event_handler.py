__author__ = 'joel'
import json
import requests
from django.conf import settings
import zmq
from device.message import zmqclient


class RawEventHandler(object):
    __send_to_hub = True
    __socket = None

    def __init__(self, send_to_hub=True):
        if send_to_hub is False:
            self.__send_to_hub = False

    def connect(self):
        if self.__socket is not None:
            return True

        if zmqclient.socket is None:
            print('Connecting ...')
            try:
                zmqclient.context = zmq.Context()
                zmqclient.socket = zmqclient.context.socket(zmq.PUB)
                zmqclient.socket.bind("tcp://" + settings.HUB_HOST + ":5556")

                # In case this is a new socket we need to sleep.
                from time import sleep
                sleep(0.5)

                self.__socket = zmqclient.socket
            except Exception as e:
                print('error while connecting')
                print(e)
                return False

        return True

    @property
    def socket(self):
        return self.__socket

    def __call__(self, raw_command, controller_id=None, cid=None):
        if not self.__send_to_hub:
            print(raw_command)
            return None

        if self.socket is None:
            self.connect()

        try:
            # compile and send message
            self.socket.send_string(
                "raw_event:" + raw_command
            )
        except Exception as e:
            print('ERROR while trying to publish message', raw_command)
            print(e)
            return False

        return True

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
            print('success', raw_command)
        except Exception:
            print('COULD NOT send to hub')
            print('... log:')
            print('API url', settings.HUB_API_URL)
            print('Endpoint url:', endpoint_url)
            print('Raw command', raw_command)

        return True
