from django.utils.translation import gettext_lazy as _
from django.db import models


class Timer(models.Model):
    DAY_OF_WEEK_MONDAY = 1
    DAY_OF_WEEK_TUESDAY = 2
    DAY_OF_WEEK_WEDNESDAY = 3
    DAY_OF_WEEK_THURSDAY = 4
    DAY_OF_WEEK_FRIDAY = 5
    DAY_OF_WEEK_SATURDAY = 6
    DAY_OF_WEEK_SUNDAY = 7

    DAY_OF_WEEK_CHOICES = (
        (DAY_OF_WEEK_MONDAY, _('Monday')),
        (DAY_OF_WEEK_TUESDAY, _('Tuesday')),
        (DAY_OF_WEEK_WEDNESDAY, _('Wednesday')),
        (DAY_OF_WEEK_THURSDAY, _('Thursday')),
        (DAY_OF_WEEK_FRIDAY, _('Friday')),
        (DAY_OF_WEEK_SATURDAY, _('Saturday')),
        (DAY_OF_WEEK_SUNDAY, _('Sunday'))
    )

    day_of_week = models.PositiveSmallIntegerField(max_length=1, choices=DAY_OF_WEEK_CHOICES, null=True, blank=True, default=None)


class TimerTimeIntervals(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    timer = models.ForeignKey(Timer, related_name='intervals')

