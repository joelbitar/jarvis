import json
import os
from datetime import timedelta
from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from django.test.client import Client
from django.core.urlresolvers import reverse

from event.receiver import Receiver
from button.models import Button, ButtonLog

from event.models import Signal, Sender

from sensor.models import Sensor, SensorLog

from device.tests import HasLoggedInClientBase

class SignalTestsHelper(TestCase):
    def helper_parse_event(self, *raw_command_strings):
        r = Receiver()
        signals = []

        for raw_command_string in raw_command_strings:
            signal, unit = r.act_on_raw_event_string(raw_command_string)
            signals.append(signal)

        return signals


class RecentSignalsTests(SignalTestsHelper, HasLoggedInClientBase):
    def setUp(self):
        super(RecentSignalsTests, self).setUp()

        for i in range(50):
            self.helper_parse_event(
                "class:command;protocol:arctech;model:selflearning;house:2887766;unit:1;group:0;method:turnon;"
            )

    def test_should_get_the_fifty_most_recent(self):
        self.helper_parse_event(
            "class:command;protocol:arctech;model:selflearning;house:2887766;unit:1;group:0;method:turnon;"
        )

        self.assertEqual(
            Signal.objects.all().count(),
            51
        )

        r = self.get_json_response(
            'signals-recent'
        )

        self.assertEqual(
            len(r),
            50
        )

    def test_should_get_name(self):
        Button.objects.update(
            name='TEST name'
        )
        r = self.get_json_response(
            'signals-recent'
        )

        signal = r[0]

        self.pretty_print_json(signal)

        self.assertEqual(
            signal['sender']['name'],
            'TEST name'
        )

    def test_should_get_most_recent_with_all_useful_data(self):
        r = self.get_json_response(
            'signals-recent'
        )

        signal = r[0]

        """
        {
    "code": null,
    "created": "2015-08-27T16:58:05.267503Z",
    "event_class": "command",
    "group": "0",
    "house": "2887766",
    "humidity": null,
    "id": 1,
    "identifier": null,
    "method": "turnon",
    "model": "selflearning",
    "protocol": "arctech",
    "raw_command": "class:command;protocol:arctech;model:selflearning;house:2887766;unit:1;group:0;method:turnon;",
    "sender": {
        "button": {
            "archived": false,
            "button_type": 1,
            "created": "2015-08-27T16:58:05.267864Z",
            "id": 1,
            "name": ""
        },
        "code": null,
        "created": "2015-08-27T16:58:05.267199Z",
        "house": "2887766",
        "id": 1,
        "identifier": null,
        "last_signal_received": "2015-08-27T16:58:05.269636Z",
        "sensor": null,
        "unit": "1"
    },
    "temp": null,
    "unit": "1"
}

        """

        self.assertIsNotNone(
            signal['sender']
        )

        self.assertIsNotNone(
            signal['sender']['button']
        )

        self.assertIsNone(
            signal['sender']['sensor']
        )



class ReceiveSignalsWithWeirdStuff(SignalTestsHelper):
    def test_minus_weird_sensor(self):
        signals = [
            'class:sensor;protocol:fineoffset;id:33;model:temperaturehumidity;humidity:53;temp:-113.0;'
        ]
        self.helper_parse_event(
            *signals
        )

        self.assertEqual(
            len(signals),
            Sensor.objects.all().count()
        )


class CreateSpecificModelInstanceTests(SignalTestsHelper):
    def test_create_a_specific_model_instance_when_button_on(self):
        self.helper_parse_event(
            'class:command;protocol:arctech;model:selflearning;house:2887766;unit:1;group:0;method:turnon;'
        )

        self.assertEqual(
            1,
            Button.objects.all().count()
        )

    def test_create_a_specific_model_instance_when_door_sensor(self):
        self.helper_parse_event(
            'class:command;protocol:arctech;model:selflearning;house:48810982;unit:11;group:0;method:turnon;'
        )

        self.assertEqual(
            1,
            Button.objects.all().count()
        )

    def test_create_for_motion_sensor(self):
        self.helper_parse_event(
            'class:command;protocol:arctech;model:selflearning;house:16504526;unit:10;group:0;method:turnon;'
        )

        self.assertEqual(
            1,
            Button.objects.all().count()
        )

    def test_create_for_button_off(self):
        self.helper_parse_event(
            'class:command;protocol:arctech;model:selflearning;house:15190034;unit:11;group:0;method:turnoff;'
        )

        self.assertEqual(
            1,
            Button.objects.all().count()
        )

    def test_create_only_one_button_when_both_on_and_off_signals_are_sent(self):
        self.helper_parse_event(
            'class:command;protocol:arctech;model:selflearning;house:15190034;unit:11;group:0;method:turnon;'
            'class:command;protocol:arctech;model:selflearning;house:15190034;unit:11;group:0;method:turnoff;',
        )

        self.assertEqual(
            1,
            Button.objects.all().count()
        )

        self.assertEqual(
            1,
            ButtonLog.objects.all().count()
        )

    def test_create_only_one_sensor_when_two_different_are_sent(self):
        signals = self.helper_parse_event(
            'class:sensor;protocol:fineoffset;id:135;model:temperaturehumidity;humidity:44;temp:21.1;',
            'class:sensor;protocol:fineoffset;id:135;model:temperaturehumidity;humidity:53;temp:21.1;'
        )

        self.assertEqual(
            1,
            Sensor.objects.all().count()
        )

        sensor = Sensor.objects.all()

    def test_create_sensor_log_events(self):
        self.helper_parse_event(
            'class:sensor;protocol:fineoffset;id:135;model:temperaturehumidity;humidity:44;temp:21.1;',
            'class:sensor;protocol:fineoffset;id:135;model:temperaturehumidity;humidity:53;temp:21.1;'
            'class:sensor;protocol:fineoffset;id:135;model:temperaturehumidity;humidity:53;temp:21.1;'
            'class:sensor;protocol:fineoffset;id:135;model:temperaturehumidity;humidity:44;temp:21.1;',
        )

        self.assertEqual(
            1,
            Sensor.objects.all().count()
        )

        self.assertEqual(
            1,
            SensorLog.objects.all().count()
        )

        sensor = Sensor.objects.all()[0]

        self.assertEqual(
            sensor.logs.all().count(),
            SensorLog.objects.all().count()
        )

    def test_create_sensor_log_event_should_add_id_to_event(self):
        self.helper_parse_event(
            'class:sensor;protocol:fineoffset;id:135;model:temperaturehumidity;humidity:44;temp:21.1;',
        )

        self.assertEqual(
            Signal.objects.all().count(),
            1
        )

        signal = Signal.objects.all()[0]

        self.assertEqual(
            signal.identifier,
            "135"
        )

        sensor = Sensor.objects.get(pk=1)

        self.assertEqual(
            sensor.identifier,
            "135"
        )

    def test_create_sensor_log_event_should_not_set_id_as_pk(self):
        self.helper_parse_event(
            'class:sensor;protocol:fineoffset;id:135;model:temperaturehumidity;humidity:44;temp:21.1;',
        )
        signal = Signal.objects.all()[0]

        self.assertEqual(
            signal.pk,
            1
        )

    def test_different_ids_should_create_multiple_sensors(self):
        self.helper_parse_event(
            'class:sensor;protocol:fineoffset;id:135;model:temperaturehumidity;humidity:44;temp:21.1;',
            'class:sensor;protocol:fineoffset;id:155;model:temperaturehumidity;humidity:44;temp:21.1;',
            'class:sensor;protocol:fineoffset;id:155;model:temperaturehumidity;humidity:44;temp:21.1;',
            'class:sensor;protocol:fineoffset;id:135;model:temperaturehumidity;humidity:44;temp:21.1;',
            'class:sensor;protocol:fineoffset;id:155;model:temperaturehumidity;humidity:44;temp:21.1;',
        )

        self.assertEqual(
            Sensor.objects.all().count(),
            2
        )


# Create your tests here.
class TestParseRawSignal(TestCase):
    def test_parse_event_and_should_create_sender_first_time(self):
        r = Receiver()
        r.parse_raw_event('class:command;protocol:arctech;model:selflearning;house:2887766;unit:1;group:0;method:turnon;')
        self.assertEqual(Signal.objects.all().count(), 1)
        self.assertEqual(Sender.objects.all().count(), 1)

        r.parse_raw_event('class:command;protocol:arctech;model:selflearning;house:2887766;unit:1;group:0;method:turnon;')
        self.assertEqual(Signal.objects.all().count(), 2)
        self.assertEqual(Sender.objects.all().count(), 1)

        e = Signal.objects.all()[0]

        self.assertEqual(e.event_class, 'command')
        self.assertEqual(e.protocol, 'arctech')
        self.assertEqual(e.model, 'selflearning')
        self.assertEqual(e.house, '2887766')
        self.assertEqual(e.code, None)
        self.assertEqual(e.unit, '1')
        self.assertEqual(e.group, '0')
        self.assertEqual(e.method, 'turnon')


class SignalsAndUnitCreationTests(SignalTestsHelper):
    def test_when_sending_multiple_signals_from_the_same_button_only_one_button_should_be_activate(self):
        self.helper_parse_event(
            'class:command;protocol:arctech;model:selflearning;house:15190034;unit:11;group:0;method:turnon;',
            'class:command;protocol:sartano;model:codeswitch;code:1010011011;method:turnoff;',
        )

        # Before setup
        self.assertEqual(
            2,
            Sender.objects.all().count(),
        )
        self.assertEqual(
            2,
            Signal.objects.all().count()
        )
        self.assertEqual(
            2,
            Button.objects.all().count()
        )

        self.assertEqual(
            2,
            ButtonLog.objects.all().count()
        )

        # Set up so that two senders are connected to one button

        duplicated_sender = Sender.objects.get(code="1010011011")
        duplicated_button = duplicated_sender.button

        self.assertIsInstance(
            duplicated_button,
            Button
        )

        duplicated_button.delete()

        primary_button = Button.objects.all()[0]

        primary_button.senders.add(duplicated_sender)
        primary_button.name = 'Primary button'
        primary_button.save()

        # Clear stuff
        ButtonLog.objects.all().delete()
        Signal.objects.all().delete()

        # Set the previous signals to a long time ago..
        Sender.objects.all().update(
            last_signal_received=timezone.now() - timedelta(hours=1)
        )

        # Do the REAL tests
        events = self.helper_parse_event(
            'class:command;protocol:arctech;model:selflearning;house:15190034;unit:11;group:0;method:turnon;',
            'class:command;protocol:sartano;model:codeswitch;code:1010011011;method:turnoff;',
        )

        # After setup
        self.assertEqual(
            2,
            Sender.objects.all().count(),
            'No new senders should be created'
        )
        self.assertEqual(
            2,
            Signal.objects.all().count(),
            'Two Singals should have been created'
        )
        self.assertEqual(
            len(events),
            2
        )

        self.assertEqual(
            1,
            Button.objects.all().count(),
            'Since the primary button have TWO senders no new buttons should be created automatically'
        )

        button = Button.objects.all()[0]
        self.assertEqual(
            2,
            button.senders.all().count(),
        )

        """
        In the 'propagate' call somewhere, perhaps in the button. we shall check if any of the senders
        """
        self.assertEqual(
            1,
            ButtonLog.objects.all().count(),
            'Since the primary button has two senders only ONE should be activated and thus only one log event.'
        )

        # Check that both events should have the same button
        for event in events:
            self.assertIsNone(
                event.sender.sensor
            )

            active_button = event.sender.button

            self.assertIsInstance(
                active_button,
                Button
            )

            self.assertEqual(
                active_button.pk,
                primary_button.pk
            )

    def test_values_not_present_in_event_should_be_set_to_null(self):
        raw_event = 'class:command;protocol:arctech;model:selflearning;group:0;method:turnon;'
        r = Receiver()
        signal = r.parse_raw_event(raw_event)

        sender = signal.sender

        self.assertIsNone(sender.unit)
        self.assertIsNone(sender.code)
        self.assertIsNone(sender.identifier)
        self.assertIsNone(sender.house)

    # For an error where senders were edited
    def test_should_create_only_one_sender_when_signal_has_been_saved_and_set_property_as_empty_string(self):
        raw_event = 'class:command;protocol:arctech;model:selflearning;house:15190034;unit:11;group:0;method:turnon;'

        r = Receiver()

        signal = r.parse_raw_event(raw_event)

        sender = signal.sender
        sender.code = ""
        sender.save()

        signal = r.parse_raw_event(raw_event)

        self.assertEqual(
            Sender.objects.all().count(),
            1,
            "Only one sender should have been created."
        )

        self.assertEqual(
            signal.sender.pk,
            1
        )

    def test_senders_should_always_have_null_values_instead_of_empty_strings_on_important_places(self):
        r = Receiver()
        signal = r.parse_raw_event('class:command;protocol:arctech;model:selflearning;house:15190034;unit:11;group:0;method:turnon;')

        self.assertIsNone(
            signal.sender.code,
            'If raw event parsing does not have a parameter it should be set to None'
        )
        self.assertIsNone(
            signal.sender.identifier,
            'If raw event parsing does not have a parameter it should be set to None'
        )

        sender = signal.sender
        sender.unit = ""
        sender.code = ""
        sender.identifier = ""
        sender.save()

        self.assertIsNone(sender.unit)
        self.assertIsNone(sender.code)
        self.assertIsNone(sender.identifier)


class TestSignalEndPoints(TestCase):
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

        self.assertEqual(Signal.objects.all().count(), 1)
        self.assertEqual(Sender.objects.all().count(), 1)

        e = Signal.objects.all()[0]

        self.assertEqual(e.event_class, 'command')
        self.assertEqual(e.protocol, 'arctech')
        self.assertEqual(e.model, 'selflearning')
        self.assertEqual(e.house, '2887766')
        self.assertEqual(e.code, None)
        self.assertEqual(e.unit, '1')
        self.assertEqual(e.group, '0')
        self.assertEqual(e.method, 'turnon')

    def test_should_create_all_required_models_when_receiving_through_web_api(self):
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
        self.assertEqual(
            Sender.objects.all().count(),
            1
        )
        self.assertEqual(
            Button.objects.all().count(),
            1
        )
        self.assertEqual(
            ButtonLog.objects.all().count(),
            1
        )


class TestReadSignalsTXTFileAndCheckSignalModelContent(TestCase):
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
            event = Signal.objects.get(pk=e.pk)

            # Go thgourh the line and check that all the posts are set.
            for keyvalue in line.split(';'):
                if not keyvalue:
                    continue

                key, value = keyvalue.split(':')

                key = receiver.sanitize_key(key)

                self.assertEqual(
                    str(getattr(event, key)),
                    str(value)
                )