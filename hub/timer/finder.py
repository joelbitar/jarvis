__author__ = 'joel'
from datetime import datetime
from datetime import time
from timer.models import Timer
from timer.models import TimerTimeIntervals
from django.db.models import Q


class LookupTimeMixin(object):
    lookup_datetime = None
    __lookup_time = None

    @property
    def lookup_time(self):
        if self.__lookup_time is not None:
            return self.__lookup_time

        self.__lookup_time = time(
            hour=self.lookup_datetime.hour,
            minute=self.lookup_datetime.minute
        )

        return self.__lookup_time


class FinderResult(LookupTimeMixin):
    __instance = None

    def __init__(self, lookup_datetime, instance):
        self.lookup_datetime = lookup_datetime
        self.__instance = instance

    def matches_start(self):
        raise NotImplementedError()

    def matches_end(self):
        raise NotImplementedError()

    @property
    def instance(self):
        return self.__instance

    @property
    def is_start(self):
        return self.matches_start()

    @property
    def is_end(self):
        return self.matches_end()


class TimerFinderResult(FinderResult):
    def matches_start(self):
        return self.instance.intervals.filter(
            start_time = self.lookup_time
        ).exists()

    def matches_end(self):
        print('Intervals::::::::::::')
        return self.instance.intervals.filter(
            end_time = self.lookup_time
        ).exists()


class FinderBase(LookupTimeMixin):
    finder_result_class = FinderResult

    def __init__(self, lookup_datetime=None):
        self.lookup_datetime = lookup_datetime or datetime.now()

    def search(self):
        raise NotImplementedError

    def find(self):
        for instance in self.search():
            yield self.finder_result_class(
                lookup_datetime=self.lookup_datetime,
                instance=instance
            )
        return


class TimerFinder(FinderBase):
    finder_result_class = TimerFinderResult

    def search(self):
        timers = Timer.objects.filter(
            Q(intervals__start_time=self.lookup_time) |
            Q(intervals__end_time=self.lookup_time)
        )
        days_of_week = {
            0: 'dow_monday',
            1: 'dow_tuesday',
            2: 'dow_wednesday',
            3: 'dow_thursday',
            4: 'dow_friday',
            5: 'dow_saturday',
            6: 'dow_sunday',
        }
        dow_attribute_name = days_of_week.get(
            self.lookup_datetime.weekday()
        )

        interval_query = Q(
            Q(intervals__start_time=self.lookup_time) |
            Q(intervals__end_time=self.lookup_time)
        )

        return Timer.objects.filter(
            Q(
                Q(weekday_dependent=False),
                interval_query
            ) |
            Q(
                Q(weekday_dependent=True),
                Q(
                    **{
                        dow_attribute_name: True
                    }
                ),
                interval_query
            )
        )

