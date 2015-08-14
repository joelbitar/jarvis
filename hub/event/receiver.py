# Class that receives raw events
from event.models import Signal
from event.models import Sender 

from django.utils import timezone
from datetime import timedelta

from button.models import Button
from sensor.models import Sensor


class Receiver(object):
    __event = None

    def __init__(self):
        self.__event = None

    @property
    def event(self):
        return self.event

    def get_or_create_sender(self, event):
        sender_identifiers = {}

        # Fetch attributes from the event and try to get
        for attribute_name in ['house', 'unit', 'code', 'identifier']:
            event_attribute_value = getattr(event, attribute_name)
            sender_identifiers[attribute_name] = event_attribute_value

        try:
            return Sender.objects.get(
                **sender_identifiers
            )
        except Sender.MultipleObjectsReturned:
            #Todo: Log error.
            return None
        except Sender.DoesNotExist:
            sender = Sender(
                **sender_identifiers
            )
            sender.save()

            return sender

    def get_or_create_unit(self, signal):
        """
        Returns a Button or Sensor event
        :return:
        """
        unit = signal.sender.get_unit()

        if unit is not None:
            return unit

        if signal.event_class == 'command' and signal.method in ['turnoff', 'turnon']:
            unit = Button()

        if signal.event_class == 'sensor' and signal.model in ['temperaturehumidity']:
            unit = Sensor()
            # Add specific stuff for sensors.
            unit.identifier = signal.identifier

        if unit is None:
            print('could not identify unit', signal.raw_command)
            print('class', signal.event_class, 'method', signal.method)

        unit.save()
        unit.senders.add(signal.sender)
        unit.save()

        return unit

    def sanitize_key(self, key):
        if key == 'class':
            key = 'event_class'

        if key == 'id':
            key = 'identifier'

        return key

    def sanitize_value(self, value):
        return value

    def parse_raw_event(self, raw_event_string):
        signal = Signal(
            raw_command=raw_event_string
        )

        for event_part in raw_event_string.split(';'):
            if event_part == "":
                continue

            key, value = event_part.split(':')

            key = self.sanitize_key(key)
            value = self.sanitize_value(value)

            setattr(signal, key, value)

        signal.sender = self.get_or_create_sender(signal)
        signal.created = timezone.now()
        signal.save()

        return signal

    def act_on_raw_event_string(self, raw_event_string):
        signal = self.parse_raw_event(raw_event_string=raw_event_string)

        unit = self.get_or_create_unit(signal)

        recent_senders = unit.senders.filter(
            last_signal_received__range=[
                timezone.now() - timedelta(seconds=1),
                timezone.now()
            ]
        )

        if recent_senders.count() > 0:
            return signal, unit

        # set last_signal received on Sender.
        sender = signal.sender
        sender.last_signal_received = timezone.now()
        sender.save()

        # Propagate event
        signal.propagate()
        # Log event and in logging
        unit.log(signal=signal)

        return signal, unit

    def __call__(self, raw_event_string):
        pass

