import json
import os
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from event.receiver import Receiver

from event.models import Event, Sender


# Create your tests here.
class TestParseRawEvent(TestCase):
    def test_parse_event_and_should_create_sender_first_time(self):
        r = Receiver()
        r.parse_raw_event('class:command;protocol:arctech;model:selflearning;house:2887766;unit:1;group:0;method:turnon;')
        self.assertEqual(Event.objects.all().count(), 1)
        self.assertEqual(Sender.objects.all().count(), 1)

        r.parse_raw_event('class:command;protocol:arctech;model:selflearning;house:2887766;unit:1;group:0;method:turnon;')
        self.assertEqual(Event.objects.all().count(), 2)
        self.assertEqual(Sender.objects.all().count(), 1)

        e = Event.objects.all()[0]

        self.assertEqual(e.event_class, 'command')
        self.assertEqual(e.protocol, 'arctech')
        self.assertEqual(e.model, 'selflearning')
        self.assertEqual(e.house, '2887766')
        self.assertEqual(e.code, None)
        self.assertEqual(e.unit, '1')
        self.assertEqual(e.group, '0')
        self.assertEqual(e.method, 'turnon')


class TestEventEndPoints(TestCase):
    def setUp(self):
        self.client = Client()

    def test_should_return_bad_request_if_no_raw_parameter_was_set(self):
        response = self.client.post(
            reverse('event'),
            json.dumps({
                'rawww': 'class:command;protocol:arctech;model:selflearning;house:2887766;unit:1;group:0;method:turnon;',
            }),
            content_type='application/json'
        )

        self.assertEqual(
            400,
            response.status_code
        )

    def test_should_be_able_to_receive_a_json_to_event_handler_view(self):
        response = self.client.post(
            reverse('event'),
            json.dumps({
                'raw': 'class:command;protocol:arctech;model:selflearning;house:2887766;unit:1;group:0;method:turnon;',
            }),
            content_type='application/json'
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(Event.objects.all().count(), 1)
        self.assertEqual(Sender.objects.all().count(), 1)

        e = Event.objects.all()[0]

        self.assertEqual(e.event_class, 'command')
        self.assertEqual(e.protocol, 'arctech')
        self.assertEqual(e.model, 'selflearning')
        self.assertEqual(e.house, '2887766')
        self.assertEqual(e.code, None)
        self.assertEqual(e.unit, '1')
        self.assertEqual(e.group, '0')
        self.assertEqual(e.method, 'turnon')


class TestReadEventsTXTFileAndCheckEventModelContent(TestCase):
    def setUp(self):
        self.events_txt_file_content = open(
            os.path.join(
                settings.BASE_DIR, 'events.txt'
            )
        ).read()

    def test_receiver_change_name_from_class_to_event_class(self):
        self.assertEqual(
            Receiver().sanitize_key('class'),
            'event_class'
        )

    def test_read_events_txt_file_and_check_created_event(self):
        receiver = Receiver()

        for line in self.events_txt_file_content.split('\n'):
            if not line:
                continue

            if line.find('#') == 0:
                continue

            e = receiver.parse_raw_event(
                line
            )

            # Refresh events to get a copy from the database
            event = Event.objects.get(pk=e.pk)

            # Go thgourh the line and check that all the posts are set.
            for keyvalue in line.split(';'):
                if not keyvalue:
                    continue

                key, value = keyvalue.split(':')

                if key == 'class':
                    key = 'event_class'

                self.assertEqual(
                    str(getattr(event, key)),
                    str(value)
                )