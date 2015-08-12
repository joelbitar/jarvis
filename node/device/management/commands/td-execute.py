__author__ = 'joel'

from django.core.management.base import BaseCommand, CommandError
import zmq

from django.conf import settings
from device.message.command import DeviceCommandMessage


class Command(BaseCommand):
    help = 'Executes commands listens to ZMQ messages'

    def handle(self, *args, **options):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)

        socket.bind("tcp://*:5556")

        print('Listening to messages, node name:', settings.NODE_NAME)
        socket.setsockopt_string(zmq.SUBSCRIBE, settings.NODE_NAME)

        message_prefix_length = len(settings.NODE_NAME)

        while True:
            complete_message = socket.recv_string()

            msg = DeviceCommandMessage(
                complete_message[message_prefix_length:]
            )

            msg.decode()
            msg.execute()


