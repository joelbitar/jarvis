from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save


class Sensor(models.Model):
    name = models.CharField(max_length=56, default='', blank=True)

    humidity = models.SmallIntegerField(null=True, default=None, blank=True)
    temperature = models.DecimalField(max_digits=3, decimal_places=1, null=True, default=None, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def log(self, signal):
        self.humidity = int(signal.humidity)
        self.temperature = int(signal.temp)
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


class SensorLog(models.Model):
    humidity = models.SmallIntegerField(null=True, blank=True, default=None)
    temperature = models.SmallIntegerField(null=True, blank=True, default=None)

    sensor = models.ForeignKey(Sensor, related_name='logs')
    created = models.DateTimeField(auto_now_add=True)


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

