__author__ = 'joel'
import json
import requests
import re
from django.conf import settings
import zmq
from device.message import zmqclient

from django.utils import timezone


class RawEventHandler(object):
    __send_to_hub = True
    __socket = None
    __accept_event_regexp = None
    __recent_signals = None

    def __init__(self, send_to_hub=True):
        if send_to_hub is False:
            self.__send_to_hub = False

        self.__accept_event_regexp = re.compile(
            "(class:command;protocol:arctech)|(class:sensor)"
        )

        self.__recent_signals = []

    @property
    def recent_signals(self):
        return self.__recent_signals

    def connect(self):
        if self.__socket is not None:
            return True

        if zmqclient.socket is None:
            print('Connecting ...')
            try:
                zmqclient.context = zmq.Context()
                zmqclient.socket = zmqclient.context.socket(zmq.PUB)
                zmqclient.socket.connect("tcp://" + settings.HUB_HOST + ":5556")

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

    def should_send_event(self, raw_event):
        if not self.__accept_event_regexp.match(raw_event):
            return False

        # Only if we accept through regex
        if self.has_been_recently_been_received(raw_event):
            return False

        return True

    def add_to_recent_signals(self, raw_command, timestamp=None):
        self.__recent_signals.insert(
            0,
            (raw_command, timestamp or timezone.now())
        )

        self.__recent_signals = self.__recent_signals[:10]

    def has_been_recently_been_received(self, raw_command):
        for recent_signal, received in self.__recent_signals:
            if recent_signal == raw_command:
                delta = timezone.now() - received
                # If this was sent less than 0.5 seconds ago
                if delta.microseconds < 500:
                    return True

        return False


    def __call__(self, raw_command, controller_id=None, cid=None):
        if not self.__send_to_hub:
            print(raw_command)
            return None

        if not self.should_send_event(raw_command):
            print('Ignoring command', raw_command)
            return None

        if self.socket is None:
            self.connect()

        try:
            # compile and send message
            self.socket.send_string(
                "raw_event:" + raw_command
            )
            self.add_to_recent_signals(raw_command)
            print('Sent: ', raw_command)
        except Exception as e:
            print('ERROR while trying to publish message', raw_command)
            print(e)
            return False

        return True
