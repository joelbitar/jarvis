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

        socket.bind("tcp://*:5557")

        #socket.connect("tcp://{address}:5557".format(
        #    address=settings.HUB_HOST
        #))

        #node_name = settings.NODE_NAME
        node_name = "command:"

        print('Listening to messages, filter:', node_name)
        socket.setsockopt_string(zmq.SUBSCRIBE, node_name)

        message_prefix_length = len(node_name)

        while True:
            complete_message = socket.recv_string()

            msg = DeviceCommandMessage(
                complete_message[message_prefix_length:]
            )

            msg.decode()
            msg.execute()


