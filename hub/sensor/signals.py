from datetime import timedelta
from datetime import datetime

from django.utils import timezone
from django.db.models import Avg
from django.db.models import Min
from django.db.models import Max


class CreateMeanBase(object):
    def create_mean(self, cls, query, sensor, **kwargs):
        sensor_data = query.aggregate(
            Avg('temperature'), Min('temperature'), Max('temperature'),
            Avg('humidity'), Min('humidity'), Max('humidity')
        )

        return cls.objects.create(
            sensor=sensor,
            temperature_min=sensor_data.get('temperature__min', None),
            temperature_max=sensor_data.get('temperature__max', None),
            temperature_avg=sensor_data.get('temperature__avg', None),
            humidity_min=sensor_data.get('humidity__min', None),
            humidity_max=sensor_data.get('humidity__max', None),
            humidity_avg=sensor_data.get('humidity__avg', None),
            **kwargs
        )

    def get_query(self, sensor, search_at, **kwargs):
        from sensor.models import SensorLog

        timedelta_unit = list(kwargs.keys())[0]
        timedelta_value = kwargs.get(timedelta_unit)

        gte = {}
        lt = {}

        gte[timedelta_unit] = timedelta_value + 1
        lt[timedelta_unit] = timedelta_value

        return SensorLog.objects.filter(
            sensor=sensor,
            created__gte=search_at - timedelta(**gte),
            created__lt=search_at - timedelta(**lt)
        )

    # Check if a class instance exists.
    def is_mean_instance(self, cls, **kwargs):
        try:
            cls.objects.get(
                **kwargs
            )
            return True
        except cls.DoesNotExist:
            pass

        return False

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
        )

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
        ) + timedelta(hours=1)

        back_in_time = -1

        # Will go back in time until we find a slot where there is no hourly log until
        while True:
            back_in_time += 1

            # Check only 48 hours back in time
            if back_in_time > 48:
                break

            # If there is a hourly at this time
            if self.is_mean_instance(SensorHourly, date_time=search_hour):
                break

            # Go backwards in time and create for every hour for which there is no hourly log

            sensor_data = self.get_query(
                sensor=instance.sensor,
                search_at=search_hour,
                hours=back_in_time
            )

            if sensor_data.count() == 0:
                continue

            self.create_mean(
                cls=SensorHourly,
                sensor=instance.sensor,
                query=sensor_data,
                date_time=search_hour
            )


class CreateDaily(CreateMeanBase):
    def create_log(self, sender, instance, **kwargs):
        from sensor.models import SensorDaily

        if instance.humidity is None and instance.temperature is None:
            return None

        search_day = self.get_created_time(
            instance=instance,
            hour=False
        ) + timedelta(days=1)

        back_in_time = 0

        # Will go back in time until we find a slot where there is no hourly log until
        while True:
            back_in_time += 1

            # Check only 48 hours back in time
            if back_in_time > 3:
                break

            # If there is a hourly at this time
            if self.is_mean_instance(SensorDaily, date=search_day):
                break

            # Go backwards in time and create for every hour for which there is no hourly log

            sensor_data = self.get_query(
                sensor=instance.sensor,
                search_at=search_day,
                days=back_in_time
            )

            if sensor_data.count() == 0:
                continue

            self.create_mean(
                cls=SensorDaily,
                sensor=instance.sensor,
                query=sensor_data
            )


