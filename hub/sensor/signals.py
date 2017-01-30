from datetime import timedelta
from datetime import datetime

from django.utils import timezone
from django.db.models import Avg
from django.db.models import Min
from django.db.models import Max


class CreateMeanBase(object):
    def get_sensor_data(self, query):
        return query.aggregate(
            Avg('temperature'), Min('temperature'), Max('temperature'),
            Avg('humidity'), Min('humidity'), Max('humidity')
        )
    def create_mean(self, cls, query, log_instance, **kwargs):
        sensor_data = self.get_sensor_data(query)

        return cls.objects.create(
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

    def get_query(self, sensor, search_at, **kwargs):
        from sensor.models import SensorLog

        timedelta_unit = list(kwargs.keys())[0]
        timedelta_value = kwargs.get(timedelta_unit)

        lt = {}

        lt[timedelta_unit] = timedelta_value

        return SensorLog.objects.filter(
            sensor=sensor,
            created__gte=search_at,
            created__lt=search_at + timedelta(**lt)
        )

    # Check if a class instance exists.
    def get_mean_instance(self, cls, **kwargs):
        try:
            return cls.objects.get(
                **kwargs
            )
        except cls.DoesNotExist:
            pass

        return None

    def get_created_time(self, instance, hour):
        kwargs = {
            "year": instance.created.year,
            "month": instance.created.month,
            "day": instance.created.day,
            "hour": instance.created.hour if hour else 0,
            "minute": 0,
            "second": 0
        }

        return timezone.make_aware(
            datetime(
                **kwargs
            )
        ) + timedelta(hours=1)

    def create_log(self, sender, instance, **kwargs):
        raise NotImplementedError("Method create_log not implemented " + str(self.__class__))


class CreateHourly(CreateMeanBase):
    def create_log(self, sender, instance, **kwargs):
        from sensor.models import SensorHourly

        if instance.humidity is None and instance.temperature is None:
            return None

        search_hour = self.get_created_time(
            instance=instance,
            hour=True
        )

        # Go backwards in time and create for every hour for which there is no hourly log
        sensor_data = self.get_query(
            sensor=instance.sensor,
            search_at=search_hour,
            hours=1
        )

        if sensor_data.count() == 0:
            # No sensor data found
            raise ValueError('Could not find any sensor logs at this time')

        hourly = self.get_mean_instance(SensorHourly, date_time=search_hour)

        # If there is a hourly at this time
        if hourly is not None:
            self.update_mean(
                mean_instance=hourly,
                log_instance=instance,
                query=sensor_data
            )
            return True

        self.create_mean(
            cls=SensorHourly,
            log_instance=instance,
            query=sensor_data,
            date_time=search_hour
        )

        return True


class CreateDaily(CreateMeanBase):
    def create_log(self, sender, instance, **kwargs):
        from sensor.models import SensorDaily

        if instance.humidity is None and instance.temperature is None:
            return None

        search_day = self.get_created_time(
            instance=instance,
            hour=False
        )

        sensor_data = self.get_query(
            sensor=instance.sensor,
            search_at=search_day,
            days=1
        )

        if sensor_data.count() == 0:
            raise ValueError('Could not find sensor data')

        daily = self.get_mean_instance(SensorDaily, date=search_day)

        # If there is a daily at this time
        if daily is not None:
            self.update_mean(
                mean_instance=daily,
                log_instance=instance,
                query=sensor_data
            )
            return True

        self.create_mean(
            cls=SensorDaily,
            log_instance=instance,
            query=sensor_data,
            date=search_day
        )


