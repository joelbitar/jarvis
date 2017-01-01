from django.test import TestCase
from forecast.models import Forecast, ForecastLog

from datetime import datetime
from django.utils import timezone

from django.db.models import Q


class ForecastHelper(TestCase):
    def helper_create_forecast_object(self,reference_time=None, valid_time=None, valid_day=None, valid_hour=None, precipitation_total=None):
        if valid_time is None:
            valid_time = timezone.make_aware(
                datetime(
                    year=2015,
                    month=1,
                    day=valid_day or 1,
                    hour=valid_hour or 1
                )
            )

        return Forecast.objects.create(
            reference_time=reference_time or timezone.now(),
            valid_time=valid_time,
            t=1.3,
            tcc=5,
            lcc=0,
            mcc=1,
            hcc=1,
            tstm=0,
            r=33,
            vis=40.0,
            gust=4.3,
            pit=precipitation_total or 0.0,
            pis=0.0,
            pcat=0,
            msl=1119.4,
            wd=123,
            ws=2.3
        )


class ForecastTests(ForecastHelper):
    def test_test(self):
        self.helper_create_forecast_object()


class ForecastBasicModelTests(ForecastHelper):
    def test_when_saving_forecast_item_forecast_log_should_be_saved(self):
        t = datetime(
            year=2015,
            month=2,
            day=16,
            hour=15
        )

        f = self.helper_create_forecast_object(
            valid_time=t
        )

        self.assertEqual(
            ForecastLog.objects.all().count(),
            1
        )

    def test_when_saving_forecast_item_forecast_log_should_be_created_if_the_reference_time_is_different(self):
        vt = datetime(
            year=2015,
            month=2,
            day=16,
            hour=15
        )
        rt = datetime(
            year=2015,
            month=2,
            day=16,
            hour=15
        )
        rt2 = datetime(
            year=2015,
            month=2,
            day=16,
            hour=21
        )

        forecast1 = self.helper_create_forecast_object(
            reference_time=rt,
            valid_time=vt
        )

        forecast1.save()
        forecast1.save()
        forecast1.save()

        f = Forecast.objects.all()[0]

        self.assertEqual(
            ForecastLog.objects.all().count(),
            1
        )

        self.helper_create_forecast_object(
            reference_time=rt2,
            valid_time=vt
        )

        self.assertEqual(
            ForecastLog.objects.all().count(),
            2
        )


"""
class ForecastFillingTests(ForecastHelper):
    def test_shold_not_fill_anything_when_there_is_no_bounds_on_either_side(self):
        self.helper_create_forecast_object()
        self.assertEqual(
            Forecast.objects.all().count(),
            1
        )

    def test_should_fill_to_previous_hour_when_creating_a_new(self):
        self.helper_create_forecast_object()
        self.helper_create_forecast_object(valid_hour=6)
        self.assertEqual(
            Forecast.objects.all().count(),
            6
        )

    def test_should_fill_pit_with_a_divided_value_from_the_latest(self):
        first = self.helper_create_forecast_object()
        last = self.helper_create_forecast_object(
            valid_hour=6,
            precipitation_total=5
        )

        others = Forecast.objects.filter(
            ~Q(pk__in=[first.pk, last.pk])
        )

        self.assertEqual(
            others.count(),
            4
        )
"""

