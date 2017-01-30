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
from django.core import signals

from device.models import Room
from device.models import Placement

from sensor.signals import CreateHourly
from sensor.signals import CreateDaily


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
    temperature_latest = models.DecimalField(max_digits=4, decimal_places=1, null=True, default=None, blank=True)

    humidity_min = models.SmallIntegerField(null=True, blank=True, default=None)
    humidity_max = models.SmallIntegerField(null=True, blank=True, default=None)
    humidity_avg = models.SmallIntegerField(null=True, blank=True, default=None)
    humidity_latest = models.SmallIntegerField(null=True, blank=True, default=None)

    class Meta:
        abstract = True


class SensorHourly(SensorMeanBase):
    sensor = models.ForeignKey(Sensor, related_name='hourly')
    date_time = models.DateTimeField()


class SensorDaily(SensorMeanBase):
    sensor = models.ForeignKey(Sensor, related_name='daily')
    date = models.DateField()


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


create_hourly = CreateHourly()
post_save.connect(create_hourly.create_log, sender=SensorLog)

create_daily = CreateDaily()
post_save.connect(create_daily.create_log, sender=SensorLog)
