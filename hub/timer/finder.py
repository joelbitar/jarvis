__author__ = 'joel'
from datetime import datetime
from timer.models import Timer
from timer.models import TimerTimeIntervals

class TimerFinder(object):
    __lookup_time = None

    def __init__(self, lookup_time=None):
        self.__lookup_time = lookup_time or datetime.now()

    def find(self):
        

        return []


class FinderResult(object):
    __instance = None
    __lookup_time = None

    def __init__(self, lookup_time, instance):
        self.__lookup_time = lookup_time
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
        return None

    def matches_end(self):
        return None
