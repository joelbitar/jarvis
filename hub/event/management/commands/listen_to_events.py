__author__ = 'joel'

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import zmq
from event.receiver import Receiver


class Command(BaseCommand):
    help = 'Listen incomming events from all nodes'

    def handle(self, *args, **options):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)

        #socket.bind("tcp://*:5556")
        socket.bind("tcp://*:5556")

        socket.setsockopt_string(zmq.SUBSCRIBE, "raw_event:")
        message_prefix_length = 10

        receiver = Receiver()

        while True:
            complete_message = socket.recv_string()
            event_message = complete_message[message_prefix_length:]
            signal, unit = receiver.act_on_raw_event_string(event_message)
