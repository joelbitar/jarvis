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
from event.tests import SignalTestsHelper


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


class SensorAPITests(HasLoggedInClientBase):
    def setUp(self):
        super(SensorAPITests, self).setUp()

        self.sensor = Sensor.objects.create(
            name='test',
            active=True
        )

    def test_should_respond_with_latest_twentyfour_hours_as_default(self):
        self.sensor.temperature = 22
        self.sensor.save()

        response = self.get_json_response(
            'sensors-history'
        )

        self.assertEqual(
            len(response),
            1
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

    def test_when_there_is_multiple_sensors_we_should_produce_number_of_hours_for_all_sensors(self):
        sensor2 = Sensor.objects.create(
            name="sensor2"
        )

        sensor2.temperature = 22
        sensor2.save()

        for sensor in Sensor.objects.all():
            for i in range(2, 31):
                sensor.temperature = i - 10
                sensor.humidity = i + 10
                sensor.save()

                sensor_log = SensorLog.objects.all().order_by('-pk')[0]

                SensorLog.objects.filter(
                    pk=sensor_log.pk
                ).update(
                    created=timezone.now() - timedelta(hours=i - 1)
                )

                log_entry = SensorLog.objects.get(pk=sensor_log.pk)
                log_entry.save()

        self.assertEqual(
            SensorHourly.objects.all().count(),
            Sensor.objects.all().count() * 30
        )

        response = self.get_json_response(
            'sensors-history',
            extra_url='?hours=24'
        )

        self.assertEqual(
            len(response),
            Sensor.objects.all().count() * 24
        )

    def test_should_be_correct_computations_and_all_values_in_json_response(self):
        for temperature, humidity in ((20, 50), (29, 60), (23, 58)):
            self.sensor.temperature = temperature
            self.sensor.humidity = humidity
            self.sensor.save()


        self.assertEqual(
            SensorLog.objects.all().count(),
            3
        )

        response = self.get_json_response(
            'sensors-history',
            extra_url='?hours=24'
        )[0]

        self.assertEqual(
            response['temperature_avg'],
            "24.0"
        )

        self.assertEqual(
            response['temperature_min'],
            "20.0"
        )

        self.assertEqual(
            response['temperature_max'],
            "29.0"
        )

        self.assertEqual(
            response['temperature_latest'],
            "23.0"
        )

        self.assertEqual(
            response['humidity_avg'],
            56
        )

        self.assertEqual(
            response['humidity_min'],
            50
        )

        self.assertEqual(
            response['humidity_max'],
            60
        )

        self.assertEqual(
            response['humidity_latest'],
            58
        )

        self.assertIsNotNone(
            response['updated']
        )

        self.assertIsNotNone(
            response['date_time']
        )

    def test_should_produce_temperature_and_humidity_history(self):
        self.sensor.temperature = -20
        self.sensor.humidity = 59
        self.sensor.save()

        self.assertEqual(
            SensorLog.objects.all().count(),
            1
        )

        for i in range(2, 31):
            self.sensor.temperature = i - 10
            self.sensor.humidity = i + 10
            self.sensor.save()

            SensorLog.objects.filter(
                pk=i
            ).update(
                created=timezone.now() - timedelta(hours=i - 1)
            )

            log_entry = SensorLog.objects.get(pk=i)
            log_entry.save()

        self.assertEqual(
            SensorHourly.objects.all().count(),
            30
        )

        find_ago_timestamp = timezone.now() - timedelta(hours=24)

        self.assertEqual(
            SensorHourly.objects.filter(date_time__gte=find_ago_timestamp).count(),
            24
        )

        response = self.get_json_response(
            'sensors-history',
            extra_url='?hours=24'
        )

        self.assertEqual(
            len(response),
            24
        )

        self.assertIsNotNone(
            response[0].get('date_time')
        )
        self.assertIsNone(
            response[0].get('date')
        )

        response = self.get_json_response(
            'sensors-history',
            extra_url='?days=2'
        )

        self.assertEqual(
            len(response),
            2
        )

        self.assertIsNotNone(
            response[0].get('date')
        )
        self.assertIsNone(
            response[0].get('date_time')
        )

        self.assertEqual(
            len(
                self.get_json_response(
                    'sensor-history',
                    kwargs={
                        'sensor_pk': self.sensor.pk
                    },
                    extra_url='?hours=24'
                )
            ),
            24
        )

        self.assertEqual(
            len(
                self.get_json_response(
                    'sensor-history',
                    kwargs={
                        'sensor_pk': self.sensor.pk
                    },
                    extra_url='?days=2'
                )
            ),
            2
        )


class SensorMeanBatchTests(TestCase):
    def setUp(self):
        sensor = Sensor.objects.create(
            name='testsensor',
            temperature=21.0
        )

        for i in range(22, 30):
            sensor.temperature = i
            sensor.save()

        SensorLog.objects.all().update(
            created = timezone.now() - timedelta(hours=1)
        )

        SensorHourly.objects.all().delete()
        SensorDaily.objects.all().delete()

    def test_run_create_mean_values_should_create_database_entries(self):
        from sensor.management.commands.create_mean_values import CreateMeanValues
        cmv = CreateMeanValues()
        cmv.run()

        self.assertEqual(
            SensorHourly.objects.all().count(),
            1
        )

        self.assertEqual(
            SensorDaily.objects.all().count(),
            1
        )

        hourly = SensorHourly.objects.all()[0]

        self.assertEqual(
            hourly.temperature_latest,
            29
        )


class SensorMeanTests(TestCase):
    def test_should_create_a_hourly_and_a_daily_when_this_is_the_first_save_of_a_sensor(self):
        sensor = Sensor.objects.create(
            name='testsensor',
            temperature=21.0
        )

        self.assertEqual(
            SensorHourly.objects.all().count(),
            1
        )

        self.assertEqual(
            SensorDaily.objects.all().count(),
            1
        )

    def test_should_update_hourly_and_daily_when_a_sensor_is_updated(self):
        sensor = Sensor.objects.create(
            name='testsensor',
            temperature=21.0
        )

        hourly = SensorHourly.objects.get(pk=1)
        self.assertEqual(
            hourly.temperature_avg,
            Decimal(21)
        )

        sensor.temperature = 23
        sensor.save()

        hourly = SensorHourly.objects.get(pk=1)
        daily = SensorDaily.objects.get(pk=1)

        self.assertEqual(
            hourly.temperature_avg,
            Decimal(22)
        )
        self.assertEqual(
            hourly.temperature_min,
            Decimal(21)
        )
        self.assertEqual(
            hourly.temperature_max,
            Decimal(23)
        )
        self.assertEqual(
            hourly.temperature_latest,
            Decimal(23)
        )

        self.assertEqual(
            daily.temperature_avg,
            Decimal(22),
            "Did not update daily."
        )
        self.assertEqual(
            daily.temperature_min,
            Decimal(21)
        )
        self.assertEqual(
            daily.temperature_max,
            Decimal(23)
        )
        self.assertEqual(
            daily.temperature_latest,
            Decimal(23),
            "did nto set daily latest"
        )

        # Did not create more hourly or daily
        self.assertEqual(
            SensorHourly.objects.all().count(),
            1
        )
        self.assertEqual(
            SensorDaily.objects.all().count(),
            1
        )

    def test_should_not_use_older_sensor_logs_when_creating_hourly(self):
        sensor = Sensor.objects.create(
            name='testsensor',
            temperature=21.0
        )

        SensorLog.objects.all().update(
            created = timezone.now() - timedelta(hours=1)
        )

        sensor.temperature = 23
        sensor.save()

        hourly = SensorHourly.objects.get(pk=1)

        self.assertEqual(
            hourly.temperature_avg,
            Decimal(23)
        )

    def test_should_not_use_older_sensor_logs_when_creating_daily(self):
        sensor = Sensor.objects.create(
            name='testsensor',
            temperature=21.0
        )

        SensorLog.objects.all().update(
            created = timezone.now() - timedelta(days=1)
        )

        SensorDaily.objects.all().update(
            date = timezone.now() - timedelta(days=1)
        )

        first_daily = SensorDaily.objects.all()[0]

        sensor.temperature = 23
        sensor.save()

        # Should create one for this day (again)
        self.assertEqual(
            SensorDaily.objects.all().count(),
            2
        )

        daily = SensorDaily.objects.get(pk=2)

        self.assertEqual(
            daily.temperature_avg,
            Decimal(23)
        )

        self.assertEqual(
            first_daily.temperature_avg,
            Decimal(21)
        )


class SensorSignalTests(SignalTestsHelper):
    def test_should_be_able_to_create_hourly_after_processing_a_sensor_signal(self):
        signals = [
            'class:sensor;protocol:fineoffset;id:33;model:temperaturehumidity;humidity:23;temp:23.0;'
        ]

        self.helper_parse_event(
            *signals
        )

        self.assertEqual(
            Sensor.objects.all().count(),
            1
        )

        self.assertEqual(
            SensorLog.objects.all().count(),
            1
        )

        self.assertEqual(
            SensorHourly.objects.all().count(),
            1
        )

        self.assertEqual(
            SensorDaily.objects.all().count(),
            1
        )

        mean = SensorHourly.objects.all()[0]

        self.assertEqual(
            mean.temperature_latest,
            Decimal(23.0)
        )
        self.assertEqual(
            mean.temperature_avg,
            Decimal(23.0)
        )
        self.assertEqual(
            mean.temperature_min,
            Decimal(23.0)
        )
        self.assertEqual(
            mean.temperature_max,
            Decimal(23.0)
        )

        self.assertEqual(
            mean.humidity_latest,
            Decimal(23.0)
        )
        self.assertEqual(
            mean.humidity_avg,
            Decimal(23.0)
        )
        self.assertEqual(
            mean.humidity_min,
            Decimal(23.0)
        )
        self.assertEqual(
            mean.humidity_max,
            Decimal(23.0)
        )


