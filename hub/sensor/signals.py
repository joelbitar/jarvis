from datetime import timedelta
from datetime import datetime

from django.utils import timezone
from django.db.models import Avg
from django.db.models import Min
from django.db.models import Max


class CreateMeanBase(object):
    mean_cls = None
    SENSOR_CLASS_NAME_DAILY = 'SensorDaily'
    SENSOR_CLASS_NAME_HOURLY = 'SensorHourly'

    def get_sensor_data(self, query):
        return query.aggregate(
            Avg('temperature'), Min('temperature'), Max('temperature'),
            Avg('humidity'), Min('humidity'), Max('humidity')
        )

    @property
    def mean_class_name(self):
        return self.mean_cls.__name__

    @property
    def time_property_name(self):
        if self.mean_class_name == self.SENSOR_CLASS_NAME_DAILY:
            return 'date'

        if self.mean_class_name == self.SENSOR_CLASS_NAME_HOURLY:
            return 'date_time'

        raise ValueError('Could not calculate what name the property should be named for ', self.mean_class_name)

    def create_mean(self, query, log_instance, search_time):
        sensor_data = self.get_sensor_data(query)

        kwargs = {
            self.time_property_name : search_time
        }

        return self.mean_cls.objects.create(
            sensor=log_instance.sensor,
            temperature_min=sensor_data.get('temperature__min', None),
            temperature_max=sensor_data.get('temperature__max', None),
            temperature_avg=sensor_data.get('temperature__avg', None),
            temperature_latest=log_instance.temperature,
            humidity_min=sensor_data.get('humidity__min', None),
            humidity_max=sensor_data.get('humidity__max', None),
            humidity_avg=sensor_data.get('humidity__avg', None),
            humidity_latest=log_instance.humidity,
            **kwargs
        )

    def update_mean(self, mean_instance, log_instance, query):
        sensor_data = self.get_sensor_data(query)

        mean_instance.temperature_min=sensor_data.get('temperature__min', None)
        mean_instance.temperature_max=sensor_data.get('temperature__max', None)
        mean_instance.temperature_avg=sensor_data.get('temperature__avg', None)
        mean_instance.temperature_latest=log_instance.temperature
        mean_instance.humidity_min=sensor_data.get('humidity__min', None)
        mean_instance.humidity_max=sensor_data.get('humidity__max', None)
        mean_instance.humidity_avg=sensor_data.get('humidity__avg', None)
        mean_instance.humidity_latest=log_instance.humidity

        mean_instance.save()

        return mean_instance

    def get_query(self, sensor, search_at):
        from sensor.models import SensorLog
        lt = {}

        if self.mean_class_name == self.SENSOR_CLASS_NAME_HOURLY:
            lt['hours'] = 1

        if self.mean_class_name == self.SENSOR_CLASS_NAME_DAILY:
            lt['days'] = 1

        return SensorLog.objects.filter(
            sensor=sensor,
            created__gte=search_at,
            created__lt=search_at + timedelta(**lt)
        )

    # Check if a class instance exists.
    def get_mean_instance(self, search_time, sensor_log):
        kwargs = {
            self.time_property_name : search_time,
            "sensor": sensor_log.sensor
        }

        try:
            return self.mean_cls.objects.get(
                **kwargs
            )
        except self.mean_cls.DoesNotExist:
            pass

        return None

    def get_created_time(self, instance):
        kwargs = {
            "year": instance.created.year,
            "month": instance.created.month,
            "day": instance.created.day,
            "hour": instance.created.hour if self.mean_class_name == self.SENSOR_CLASS_NAME_HOURLY else 0,
            "minute": 0,
            "second": 0
        }

        return timezone.make_aware(
            datetime(
                **kwargs
            )
        ) + timedelta(hours=1)

    def create_log(self, sender, instance, **kwargs):
        if instance.humidity is None and instance.temperature is None:
            return None

        search_time = self.get_created_time(
            instance=instance
        )

        # Go backwards in time and create for every hour for which there is no hourly log
        sensor_data = self.get_query(
            sensor=instance.sensor,
            search_at=search_time
        )

        if sensor_data.count() == 0:
            # No sensor data found
            raise ValueError('Could not find any sensor logs at this time')

        mean = self.get_mean_instance(search_time=search_time, sensor_log=instance)

        # If there is a hourly at this time
        if mean is not None:
            self.update_mean(
                mean_instance=mean,
                log_instance=instance,
                query=sensor_data
            )
            return True

        self.create_mean(
            log_instance=instance,
            query=sensor_data,
            search_time=search_time
        )
        return True


class CreateHourly(CreateMeanBase):
    def __init__(self):
        from sensor.models import SensorHourly
        self.mean_cls = SensorHourly


class CreateDaily(CreateMeanBase):
    def __init__(self):
        from sensor.models import SensorDaily
        self.mean_cls = SensorDaily
