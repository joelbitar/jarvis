from django.test import TestCase

from sensor.models import Sensor, SensorLog

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
