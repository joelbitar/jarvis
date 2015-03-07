from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=56, default='', blank=True)

    humidity = models.SmallIntegerField(null=True, default=None, blank=True)
    temperature = models.SmallIntegerField(null=True, default=None, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        if self.name:
            return str(self.name)

        return str(self.pk)

    def __unicode__(self):
        if self.name:
            return self.name

        return str(self.pk)



class SensorLog(models.Model):
    humidity = models.SmallIntegerField()
    temperature = models.SmallIntegerField()

    sensor = models.ForeignKey(Sensor, related_name='logs')
    created = models.DateTimeField(auto_now_add=True)



