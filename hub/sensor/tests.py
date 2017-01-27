import os
from decimal import Decimal
from django.conf import settings
from django.test import TestCase
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.utils import timezone

from sensor.models import Sensor, SensorLog
from device.tests import HasLoggedInClientBase
from event.models import Signal, Sender
import json

from sensor.models import SensorDaily, SensorHourly


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

    def test_after_logging_on_sensor_should_have_correct_values_for_each_parameter(self):
        sensor = Sensor(
            name='testSensor'
        )
        sensor.save()

        signal = Signal.objects.create(
            temp="21.5",
            humidity="65"
        )

        sensor.log(
            signal=signal
        )

        self.assertEqual(
            str(sensor.humidity),
            signal.humidity
        )

        self.assertEqual(
            str(sensor.temperature),
            signal.temp
        )


class SensorLoggingTests(TestCase):
    def test_sensor_log_should_have_correct_values(self):
        """
        sensor = Sensor()
        sensor.name ="test sensor"
        sensor.temperature=21.5
        sensor.save()
        """

        sensor = Sensor.objects.create(
            name="test sensor",
            temperature=21.5
        )

        sensor = Sensor.objects.get(pk=sensor.pk)

        self.assertEqual(
            sensor.temperature,
            21.5
        )

        self.assertEqual(
            SensorLog.objects.all().count(),
            1
        )

        log_entry = sensor.logs.all()[0]

        self.assertEqual(
            log_entry.temperature,
            21.5
        )


class TestSensorAPI(HasLoggedInClientBase):
    def setUp(self):
        super(TestSensorAPI, self).setUp()

        self.sensor = Sensor.objects.create(
            name='test',
            active=True
        )

    def test_should_only_see_active_sensors(self):
        inactive_sensor = Sensor.objects.create(
            name='test',
        )

        r = self.logged_in_client.get(
            reverse('sensor-list')
        )

        self.assertEqual(
            len(json.loads(r.content.decode('utf-8'))),
            1
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


class SensorMeanTests(TestCase):
    def test_should_not_create_until_we_have_a_bunch_of_old_log_entries(self):
        sensor = Sensor.objects.create(
            name='testsensor',
            temperature=21.0
        )

        for temp in [22, 23, 24, 25, 26]:
            sensor.temperature = temp
            sensor.save()

        self.assertEqual(
            SensorHourly.objects.all().count(),
            0
        )

        SensorLog.objects.all().update(
            created = timezone.now() - timedelta(hours=1)
        )

        sensor.temperature = 20
        sensor.save()

        self.assertEqual(
            SensorHourly.objects.all().count(),
            1
        )

        hourly = sensor.hourly.all()[0]

        self.assertEqual(
            hourly.temperature_min,
            Decimal(21.0)
        )

        self.assertEqual(
            hourly.temperature_max,
            Decimal(26.0)
        )

        self.assertEqual(
            hourly.temperature_avg,
            Decimal(23.5)
        )

    def test_should_create_hourly_mean_values_if_when_the_latest_entry_is_created_in_a_new_hour(self):
        sensor = Sensor.objects.create(
            name='testsensor',
            temperature=21.5
        )

        SensorHourly.objects.all().delete()

        self.assertEqual(
            SensorHourly.objects.all().count(),
            0
        )

        SensorLog.objects.all().delete()
        # Backdate sensor and log entry
        sensor.save()
        SensorLog.objects.all().update(
            created = timezone.now() - timedelta(hours=1)
        )

        SensorHourly.objects.all().delete()
        SensorDaily.objects.all().delete()

        log_entry = SensorLog.objects.all()[0]

        # New temperature.
        sensor.temperature = 24.5
        sensor.save()

        # There should now be a new log entry, two in total
        self.assertEqual(
            SensorLog.objects.all().count(),
            2
        )

        # The latest log entry
        log_entry = SensorLog.objects.get(pk=3)

        # Should be created same second
        self.assertEqual(
            str(log_entry.created)[:19],
            str(sensor.updated)[:19]
        )

        self.assertEqual(
            SensorDaily.objects.all().count(),
            0
        )

        self.assertEqual(
            SensorHourly.objects.all().count(),
            1
        )

        sensor_hourly = SensorHourly.objects.all()[0]
        self.assertEqual(
            sensor_hourly.temperature_min,
            Decimal(21.5)
        )
        self.assertEqual(
            sensor_hourly.temperature_max,
            Decimal(21.5)
        )
        self.assertEqual(
            sensor_hourly.temperature_avg,
            Decimal(21.5)
        )

    def test_should_create_day_mean_values_if_when_the_latest_entry_is_created_a_day_later(self):
        sensor = Sensor.objects.create(
            name='old sensor',
            temperature=21.5
        )

        self.assertEqual(
            SensorDaily.objects.all().count(),
            0
        )

        SensorLog.objects.all().delete()

        sensor.save()
        # Backdate sensor and log entry
        SensorLog.objects.all().update(
            created = timezone.now() - timedelta(days=1)
        )


        SensorHourly.objects.all().delete()
        SensorDaily.objects.all().delete()

        # New temperature.
        sensor.temperature = 24.5
        sensor.save()

        # There should now be a new log entry, two in total
        self.assertEqual(
            SensorLog.objects.all().count(),
            2
        )

        # The latest log entry
        log_entry = SensorLog.objects.get(pk=3)

        # Should be created same second
        self.assertEqual(
            str(log_entry.created)[:19],
            str(sensor.updated)[:19]
        )

        # Should create one hourly for that day.
        self.assertEqual(
            SensorHourly.objects.all().count(),
            1
        )

        sensor_hourly = SensorHourly.objects.all()[0]
        self.assertEqual(
            sensor_hourly.temperature_min,
            21.5
        )
        self.assertEqual(
            sensor_hourly.temperature_max,
            21.5
        )
        self.assertEqual(
            sensor_hourly.temperature_avg,
            21.5
        )

        self.assertEqual(
            SensorDaily.objects.all().count(),
            1,
            "should create a daily mean"
        )

        # The daily hourly
        sensor_daily = SensorDaily.objects.all()[0]
        self.assertEqual(
            sensor_daily.temperature_min,
            21.5
        )
        self.assertEqual(
            sensor_daily.temperature_max,
            21.5
        )
        self.assertEqual(
            sensor_daily.temperature_avg,
            21.5
        )

    def test_if_multiple_log_events_are_created_should_calculate_averages_and_min_max_hourly(self):
        sensor = Sensor.objects.create(
            name='testsensor',
            temperature=21.0
        )

        for temp in [22, 23, 24, 25, 26]:
            sensor.temperature = temp
            sensor.save()

        self.assertEqual(
            SensorHourly.objects.all().count(),
            0
        )

        self.assertEqual(
            SensorLog.objects.all().count(),
            6
        )

        SensorLog.objects.all().update(
            created = timezone.now() - timedelta(hours=2)
        )

        sensor.temperature = 27
        sensor.save()

        self.assertEqual(
            SensorLog.objects.all().count(),
            7
        )

        # should only create one
        self.assertEqual(
            SensorHourly.objects.all().count(),
            1
        )

        SensorLog.objects.all().update(
            created = timezone.now() - timedelta(hours=1),
        )

        sensor.temperature = 99
        sensor.save()

        self.assertEqual(
            SensorHourly.objects.all().count(),
            2
        )

        # Test temps on both hourlsys
        first = SensorHourly.objects.get(pk=1)
        self.assertEqual(
            first.temperature_min,
            Decimal(21.0)
        )
        self.assertEqual(
            first.temperature_max,
            Decimal(26.0)
        )
        self.assertEqual(
            first.temperature_avg,
            Decimal(23.5)
        )

        # This is the one one hour ago.
        second = SensorHourly.objects.get(pk=2)
        self.assertEqual(
            second.temperature_min,
            Decimal(21.0)
        )
        self.assertEqual(
            second.temperature_max,
            Decimal(27.0)
        )
        self.assertEqual(
            second.temperature_avg,
            Decimal(24.0)
        )

    def test_if_multiple_log_events_are_created_should_calculate_averages_and_min_max_daily(self):
        sensor = Sensor.objects.create(
            name='testsensor',
            temperature=21.0
        )

        for temp in [22, 23, 24, 25, 26]:
            sensor.temperature = temp
            sensor.save()

        self.assertEqual(
            SensorHourly.objects.all().count(),
            0
        )
        self.assertEqual(
            SensorDaily.objects.all().count(),
            0
        )

        self.assertEqual(
            SensorLog.objects.all().count(),
            6
        )

        SensorLog.objects.all().update(
            created = timezone.now() - timedelta(days=2)
        )

        sensor.temperature = 27
        sensor.save()

        self.assertEqual(
            SensorLog.objects.all().count(),
            7
        )

        # should only create one
        self.assertEqual(
            SensorDaily.objects.all().count(),
            1
        )

        SensorLog.objects.all().update(
            created=timezone.now() - timedelta(days=1),
        )

        sensor.temperature = 99
        sensor.save()

        self.assertEqual(
            SensorDaily.objects.all().count(),
            2
        )

        # Test temps on both hourlsys
        first = SensorDaily.objects.get(pk=1)
        self.assertEqual(
            first.temperature_min,
            Decimal(21.0)
        )
        self.assertEqual(
            first.temperature_max,
            Decimal(26.0)
        )
        self.assertEqual(
            first.temperature_avg,
            Decimal(23.5)
        )

        # This is the one one hour ago.
        second = SensorDaily.objects.get(pk=2)
        self.assertEqual(
            second.temperature_min,
            Decimal(21.0)
        )
        self.assertEqual(
            second.temperature_max,
            Decimal(27.0)
        )
        self.assertEqual(
            second.temperature_avg,
            Decimal(24.0)
        )
    
