from django.test import TestCase
from event.tests import SignalTestsHelper

from button.models import Button, Bell
from sensor.models import Sensor
from janitor.janitor import Scruffy, ButtonJanitor, SensorJanitor

from event.models import Sender, Signal

# Create your tests here.

class CleanUpBaseTests(SignalTestsHelper):
    def setUp(self):
        signals = self.helper_parse_event(
            "class:command;protocol:arctech;model:selflearning;house:1;unit:1;group:0;method:turnon;",
            "class:command;protocol:arctech;model:selflearning;house:2;unit:1;group:0;method:turnon;",
            'class:sensor;protocol:fineoffset;id:1;model:temperaturehumidity;humidity:44;temp:21.1;',
            'class:sensor;protocol:fineoffset;id:2;model:temperaturehumidity;humidity:44;temp:21.1;',
        )

        b = Button.objects.get(pk=1)
        b.name = 'Test Button'
        b.save()

        s = Sensor.objects.get(pk=1)
        s.name = 'Test Sensor'
        s.save()


    def test_should_be_stuff_created(self):
        self.assertEqual(
            Button.objects.all().count(),
            2
        )

        self.assertEqual(
            Sensor.objects.all().count(),
            2
        )

        self.assertEqual(
            Sender.objects.all().count(),
            4
        )

class CleanUpUnusedButtons(CleanUpBaseTests):
    def test_after_cleanup_there_should_be_no_unnamed_buttons(self):
        ButtonJanitor().clean()

        self.assertEqual(
            Button.objects.all().count(),
            1
        )

        self.assertEqual(
            Sender.objects.all().count(),
            3
        )

        b = Button.objects.all()[0]

        self.assertEqual(
            b.name,
            'Test Button'
        )

        self.assertEqual(
            Button.objects.filter(name='').count(),
            0
        )

    def test_after_sensor_cleanup_there_should_be_no_unnamed_sensors(self):
        SensorJanitor().clean()

        self.assertEqual(
            Sensor.objects.all().count(),
            1
        )

        self.assertEqual(
            Sender.objects.all().count(),
            3
        )

        s = Sensor.objects.all()[0]

        self.assertEqual(
            s.name,
            'Test Sensor'
        )

        self.assertEqual(
            Sensor.objects.filter(name='').count(),
            0
        )

    def test_after_master_cleanup_there_should_be_no_unnamed_anything(self):
        Scruffy().clean()

        self.assertEqual(
            Button.objects.all().count(),
            1
        )

        self.assertEqual(
            Sensor.objects.all().count(),
            1
        )

        self.assertEqual(
            Sender.objects.all().count(),
            2
        )


