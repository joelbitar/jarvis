# Class that receives raw events
from event.models import Event
from event.models import Sender 


class Receiver(object):
    def get_or_create_sender(self, event):
        sender_identifiers = {}

        # Fetch attributes from the event and try to get
        for attribute_name in ['house', 'unit', 'code']:
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

    def parse_raw_event(self, raw_event_string):
        event = Event(
            raw_command=raw_event_string
        )

        for event_part in raw_event_string.split(';'):
            if event_part == "":
                continue

            key, value = event_part.split(':')
            setattr(event, key, value)

        event.sender = self.get_or_create_sender(event)
        event.save()



    def __call__(self, raw_event_string):
        pass

