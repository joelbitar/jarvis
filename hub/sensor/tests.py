from django.test import TestCase

from django.core.urlresolvers import reverse

from sensor.models import Sensor, SensorLog
from device.tests import HasLoggedInClientBase

import json


# Create your tests here.
class SensorModelTests(TestCase):
    def test_after_first_save_on_sensor_should_not_have_sensor_log_if_humidity_and_temperature_is_none(self):
        s = Sensor(
            name="testSensor"
        )

        s.save()

        self.assertEqual(
            SensorLog.objects.all().count(),
            0
        )

    def test_after_first_save_on_sensor_with_humidity_should_have_entry_in_log(self):
        s = Sensor(
            name="testSensor"
        )
        s.humidity = 22

        s.save()

        self.assertEqual(
            SensorLog.objects.all().count(),
            1
        )

    def test_after_first_save_on_sensor_with_temperature_should_have_entry_in_log(self):
        s = Sensor(
            name="testSensor"
        )
        s.temperature = 22

        s.save()

        self.assertEqual(
            SensorLog.objects.all().count(),
            1
        )

    def test_after_first_save_on_sensor_with_temperature_and_humidity_should_have_entry_in_log(self):
        s = Sensor(
            name="testSensor"
        )
        s.humidity = 22
        s.temperature = 22

        s.save()

        self.assertEqual(
            SensorLog.objects.all().count(),
            1
        )

    def test_after_each_save_sensor_log_should_have_an_entry(self):
        s = Sensor(
            name="testSensor"
        )

        s.save()

        for i in range(1, 9):
            s.humidity = 87
            s.temperature = 22
            s.save()

            self.assertEqual(
                SensorLog.objects.all().count(),
                i
            )


class TestSensorAPI(HasLoggedInClientBase):
    def setUp(self):
        super(TestSensorAPI, self).setUp()

        self.sensor = Sensor.objects.create(
            name='test'
        )

    def test_should_have_log_entries_in_json(self):
        self.sensor.temperature = 22
        self.sensor.humidity = 44
        self.sensor.save()

        r = self.logged_in_client.get(
            reverse('sensorlog-list', kwargs={
                'sensor_pk': self.sensor.pk
            })
        )

        self.assertEqual(
            len(json.loads(r.content.decode('utf-8'))),
            1
        )


