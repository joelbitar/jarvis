from django.utils.translation import gettext_lazy as _
from django.db import models


class Timer(models.Model):
    dow_monday = models.BooleanField(default=False, verbose_name='monday', help_text=_('Monday'))
    dow_tuesday = models.BooleanField(default=False, verbose_name='tuesday', help_text=_('Tuesday'))
    dow_wednesday = models.BooleanField(default=False, verbose_name='wednesday', help_text=_('Wednesday'))
    dow_thursday = models.BooleanField(default=False, verbose_name='thursday', help_text=_('Thursday'))
    dow_friday = models.BooleanField(default=False, verbose_name='friday', help_text=_('Friday'))
    dow_saturday = models.BooleanField(default=False, verbose_name='saturday', help_text=_('Saturday'))
    dow_sunday = models.BooleanField(default=False, verbose_name='sunday', help_text=_('Sunday'))


class TimerTimeIntervals(models.Model):
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    timer = models.ForeignKey(Timer, related_name='intervals')

