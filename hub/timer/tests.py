from django.test import TestCase
from timer.models import Timer
from timer.models import TimerTimeIntervals
from timer.finder import TimerFinder
from django.utils import timezone
from datetime import datetime
from datetime import time


class TimerFinderTestsHelper(TestCase):
    def helper_find_timers(self, year=2015, month=4, day=13, hour=10, minute=0):
        finder = TimerFinder(
            datetime(year=year, month=month, day=day, hour=hour, minute=minute)
        )

        return finder.find()

    def helper_should_find_on_lookup_day(self, day, count=1):
        self.assertEqual(
            len(TimerFinder(lookup_time=datetime(year=2015, month=4, day=day, hour=10, minute=0)).find()), 1
        )
        for i in range(day, day+7):
            self.assertEqual(
                len(TimerFinder(lookup_time=datetime(year=2015, month=4, day=i, hour=10, minute=0)).find()), 0
            )


class TimerFinderTestsBase(TimerFinderTestsHelper):
    def setUp(self):
        self.timer = Timer()

        self.timer.save()

        interval = TimerTimeIntervals()
        interval.start_time = time(hour=10, minute=0)
        interval.end_time = time(hour=12, minute=0)


class TimerFinderTests(TimerFinderTestsBase):
    def test_should_not_find_any_if_there_are_no_timers(self):
        Timer.objects.all().delete()
        self.assertEqual(
            len(self.helper_find_timers()),
            0
        )

    def test_should_find_timer_if_we_look_at_the_start_and_end_minutes(self):
        self.assertEqual(
            len(self.helper_find_timers()),
            1
        )
        self.assertEqual(
            len(self.helper_find_timers(hour=12)),
            1
        )

    def test_should_not_find_any_timers_if_we_look_at_the_in_between_minutes(self):
        self.assertEqual(
            len(self.helper_find_timers(hour=11)),
            0
        )

    def test_should_find_on_monday(self):
        self.timer.dow_monday = True
        self.timer.save()

        self.helper_should_find_on_lookup_day(13)

    def test_should_find_on_tuesday(self):
        self.timer.dow_tuesday = True
        self.timer.save()

        self.helper_should_find_on_lookup_day(14)

    def test_should_find_on_wednesday(self):
        self.timer.dow_wednesday = True
        self.timer.save()

        self.helper_should_find_on_lookup_day(15)

    def test_should_find_on_thursday(self):
        self.timer.dow_thursday = True
        self.timer.save()

        self.helper_should_find_on_lookup_day(16)

    def test_should_find_on_friday(self):
        self.timer.dow_friday = True
        self.timer.save()

        self.helper_should_find_on_lookup_day(17)

    def test_should_find_on_saturday(self):
        self.timer.dow_saturday = True
        self.timer.save()

        self.helper_should_find_on_lookup_day(19)

    def test_should_find_on_sunday(self):
        self.timer.dow_sunday = True
        self.timer.save()

        self.helper_should_find_on_lookup_day(19)


class TimerShouldKnowIfItIsStartOrEnd(TimerFinderTestsBase):
    def test_lookup_at_first_minute_and_should_know_that_it_is_start(self):
        r = self.helper_find_timers(hour=10)[0]
        self.assertEqual(
            r.start(),
            True
        )

    def test_lookup_at_last_and_should_know_that_it_is_end(self):
        r = self.helper_find_timers(hour=10)[0]
        self.assertEqual(
            r.end(),
            True
        )


