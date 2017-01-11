from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from datetime import timedelta


class ForecastBase(models.Model):
    PARAMETER_MAP = (
        ('t', 'temperature',),
        ('tcc', 'total_cloud_coverage', ),

    )
    PRECIPITATION_CATEGORY_NONE = 0
    PRECIPITATION_CATEGORY_SNOW = 1
    PRECIPITATION_CATEGORY_SNOW_AND_RAIN = 2
    PRECIPITATION_CATEGORY_RAIN = 3
    PRECIPITATION_CATEGORY_DRIZZLE = 4
    PRECIPITATION_CATEGORY_FREEZING_RAIN = 5
    PRECIPITATION_CATEGORY_FREEZING_DRIZZLE = 6
    PRECIPITATION_CATEGORY_CHOICES = (
        (PRECIPITATION_CATEGORY_NONE, 'None',),
        (PRECIPITATION_CATEGORY_SNOW, 'Snow',),
        (PRECIPITATION_CATEGORY_SNOW_AND_RAIN, 'Snow and rain',),
        (PRECIPITATION_CATEGORY_RAIN, 'Rain',),
        (PRECIPITATION_CATEGORY_DRIZZLE, 'Drizzle',),
        (PRECIPITATION_CATEGORY_FREEZING_RAIN, 'Freezing rain',),
        (PRECIPITATION_CATEGORY_FREEZING_DRIZZLE, 'Freezing drizzle',),
    )

    reference_time = models.DateTimeField()
    valid_time = models.DateTimeField()
    t = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Temperature')
    tcc = models.PositiveSmallIntegerField(verbose_name='Total cloud coverage', help_text='How much cloud coverage, 0-8')
    lcc = models.PositiveSmallIntegerField(verbose_name='Low cloud coverage', help_text='How much cloud coverage, 0-8')
    mcc = models.PositiveSmallIntegerField(verbose_name='Medium cloud coverage', help_text='How much cloud coverage, 0-8')
    hcc = models.PositiveSmallIntegerField(verbose_name='High cloud coverage', help_text='How much cloud coverage, 0-8')
    tstm = models.PositiveSmallIntegerField(verbose_name='Chance of thunder percentage')
    r = models.PositiveSmallIntegerField(verbose_name='Relative humidity')
    vis = models.PositiveIntegerField(verbose_name='Visibility')
    gust = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Gust')
    pit = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Percipitation intensity total')
    # LEGACY
    pis = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Percipitation intensity snow')
    pcat = models.PositiveSmallIntegerField(verbose_name='Percipitation category', choices=PRECIPITATION_CATEGORY_CHOICES)
    msl = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Air pressure')
    wd = models.PositiveSmallIntegerField(verbose_name='Wind direction')
    ws = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Wind velocity')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.valid_time)

    class Meta:
        abstract = True
        ordering = ['valid_time']


class Forecast(ForecastBase):
    updated = models.DateTimeField(auto_now=True)


class ForecastLog(ForecastBase):
    forecast = models.ForeignKey(Forecast, related_name='logs')


@receiver(post_save, sender=Forecast)
def create_forecast_log(sender, instance=None, created=False, **kwargs):
    if instance.logs.filter(
                reference_time=instance.reference_time
            ).exists():
        return None

    fc = ForecastLog(
        t=instance.t,
        tcc=instance.tcc,
        lcc=instance.lcc,
        mcc=instance.mcc,
        hcc=instance.hcc,
        tstm=instance.tstm,
        r=instance.r,
        vis=instance.vis,
        gust=instance.gust,
        pit=instance.pit,
        pis=instance.pis,
        pcat=instance.pcat,
        msl=instance.msl,
        wd=instance.wd,
        ws=instance.ws,

        valid_time=instance.valid_time,
        reference_time=instance.reference_time,

        forecast=instance
    )

    fc.save()

@receiver(post_save, sender=Forecast)
def fill_to_previous_hour(sender, instance=None, created=False, **kwargs):
    return None

    if not created:
        return None

    previous_forecast_entry_set = Forecast.objects.filter(
        valid_time__lt = instance.valid_time
    )

    # Check that there is any
    if not previous_forecast_entry_set.exists():
        return None

    previous_forecast_entry = previous_forecast_entry_set[0]

    time_difference = instance.valid_time - previous_forecast_entry.valid_time

    hours_difference = round(time_difference.seconds / 3600)

    print('Should calculate precipitation for the new span')

    # Step upp to the current time (not on it)
    for hour_step in range(1, hours_difference - 1):
        instance.valid_time = previous_forecast_entry.valid_time + timedelta(hours=hour_step)
        instance.pk = None
        instance.save()


