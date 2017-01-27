from decimal import Decimal

from datetime import timedelta
from datetime import datetime

from django.db import models
from django.db.models import Avg
from django.db.models import Min
from django.db.models import Max

from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from device.models import Room
from device.models import Placement


class Sensor(models.Model):
    name = models.CharField(max_length=56, default='', blank=True)

    humidity = models.SmallIntegerField(null=True, default=None, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, default=None, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    identifier = models.CharField(max_length=4, default=None, blank=True, null=True)

    active = models.BooleanField(default=False, help_text="If we should bother with the sensor")

    room = models.ForeignKey(Room, related_name='sensors', default=None, blank=True, null=True)
    placement = models.ForeignKey(Placement, related_name='sensors', default=None, blank=True, null=True)

    def log(self, signal):
        self.humidity = int(signal.humidity)
        self.temperature = Decimal(signal.temp)
        self.save()

        return True

    def __str__(self):
        if self.name:
            return str(self.name)

        return str(self.pk)

    def __unicode__(self):
        if self.name:
            return self.name

        return str(self.pk)

    class Meta:
        ordering = ('name', )


class SensorLog(models.Model):
    humidity = models.SmallIntegerField(null=True, blank=True, default=None)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, default=None, blank=True)

    sensor = models.ForeignKey(Sensor, related_name='logs')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{sensor.name} - {temp}c {humidity}%".format(
            sensor=self.sensor,
            temp=self.temperature,
            humidity=self.humidity
        )

    class Meta:
        ordering = ['-id']


class SensorMeanBase(models.Model):
    temperature_min = models.DecimalField(max_digits=4, decimal_places=1, null=True, default=None, blank=True)
    temperature_max = models.DecimalField(max_digits=4, decimal_places=1, null=True, default=None, blank=True)
    temperature_avg = models.DecimalField(max_digits=4, decimal_places=1, null=True, default=None, blank=True)
    humidity_min = models.SmallIntegerField(null=True, blank=True, default=None)
    humidity_max = models.SmallIntegerField(null=True, blank=True, default=None)
    humidity_avg = models.SmallIntegerField(null=True, blank=True, default=None)

    class Meta:
        abstract = True


class SensorHourly(SensorMeanBase):
    sensor = models.ForeignKey(Sensor, related_name='hourly')
    date_time = models.DateTimeField(auto_now_add=True)


class SensorDaily(SensorMeanBase):
    sensor = models.ForeignKey(Sensor, related_name='daily')
    date = models.DateField(auto_now_add=True)


@receiver(post_save, sender=Sensor)
def log_sensor(sender, instance, **kwargs):
    if instance.humidity is None and instance.temperature is None:
        return None

    log = SensorLog(
        humidity=instance.humidity,
        temperature=instance.temperature,
        sensor=instance
    )

    log.save()


@receiver(post_save, sender=SensorLog)
def create_hourly_log(sender, instance, **kwargs):
    if instance.humidity is None and instance.temperature is None:
        return None

    created_hour = timezone.make_aware(
        datetime(
            year=instance.created.year,
            month=instance.created.month,
            day=instance.created.day,
            hour=instance.created.hour,
            minute=0,
            second=0,
        )
    )

    search_hour = created_hour + timedelta(hours=1)

    back_in_time = -1

    # Will go back in time until we find a slot where there is no hourly log until
    while True:
        back_in_time += 1

        # Check only 48 hours back in time
        if back_in_time > 48:
            break

        # Check if there is no hourly log for this hour
        try:
            SensorHourly.objects.get(
                date_time=search_hour
            )
            break
        except SensorHourly.DoesNotExist:
            pass

        # Go backwards in time and create for every hour for which there is no hourly log

        sensor_data = SensorLog.objects.filter(
            sensor=instance.sensor,
            created__gte=search_hour - timedelta(hours=back_in_time + 1),
            created__lt=search_hour - timedelta(hours=back_in_time)
        )

        if sensor_data.count() == 0:
            continue

        sensor_data = sensor_data.aggregate(
            Avg('temperature'), Min('temperature'), Max('temperature'),
            Avg('humidity'), Min('humidity'), Max('humidity')
        )

        SensorHourly.objects.create(
            sensor=instance.sensor,
            temperature_min=sensor_data.get('temperature__min', None),
            temperature_max=sensor_data.get('temperature__max', None),
            temperature_avg=sensor_data.get('temperature__avg', None),
            humidity_min=sensor_data.get('humidity__min', None),
            humidity_max=sensor_data.get('humidity__max', None),
            humidity_avg=sensor_data.get('humidity__avg', None),
        )


