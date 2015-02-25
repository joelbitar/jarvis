from django.db import models
from event.models import Sender


class Sensor(models.Model):
    humidity = models.SmallIntegerField(null=True, default=None, blank=True)
    temperature = models.SmallIntegerField(null=True, default=None, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    senders = models.ManyToManyField(Sender, related_name='sensors')

    def log(self, signal):
        self.humidity = int(signal.humidity)
        self.temperature = int(signal.humidity)
        self.save()

        log = SensorLog(
            humidity=self.humidity,
            temperature=self.temperature,
            sensor=self
        )

        log.save()

        return log


class SensorLog(models.Model):
    humidity = models.SmallIntegerField()
    temperature = models.SmallIntegerField()

    sensor = models.ForeignKey(Sensor, related_name='logs')
    created = models.DateTimeField(auto_now_add=True)



