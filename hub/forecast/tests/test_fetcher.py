import os
import json

from django.conf import settings
from django.utils import timezone

from django.core.urlresolvers import reverse

from forecast import fetcher
from django.test import TestCase

from forecast.models import Forecast

from device.tests import HasLoggedInClientBase


class MockedSMHIFetcherBase(HasLoggedInClientBase):
    FAKE_RESPONSE_JSON_FILE_NAME = None

    def setUp(self):
        super(MockedSMHIFetcherBase, self).setUp()

        self.FAKE_RESPONSE_JSON_FILE_NAME = "1.json"

        self.fetcher = fetcher.ForecastFetcher()

        def fake_fetch_from_smhi():
            return open(
                os.path.join(
                    settings.BASE_DIR,
                    'forecast',
                    'tests',
                    'json',
                    self.FAKE_RESPONSE_JSON_FILE_NAME
                ),
                'r'
            ).read()

        self.fetcher.fetch_from_shmi = fake_fetch_from_smhi

    def run_create_entries(self, file_name=None):
        self.FAKE_RESPONSE_JSON_FILE_NAME = file_name or "1.json"
        entries = [e for e in self.fetcher.create_entries()]
        return entries

    def tearDown(self):
        self.FAKE_RESPONSE_JSON_FILE_NAME = "1.json"


class FetchFromSMHITests(MockedSMHIFetcherBase):
    def test_create_entries_should_produce_equal_number_of_units_as_there_is_timeseries(self):
        json = self.fetcher.get_parsed_result()

        entries = self.run_create_entries()

        self.assertTrue(
            Forecast.objects.all().count() > 10
        )

        self.assertEqual(
            Forecast.objects.all().count(),
            len(json['timeSeries'])
        )

    def test_create_entries_should_not_yield_duplicates(self):
        self.run_create_entries()
        created_entries = Forecast.objects.all().count()

        self.run_create_entries()

        self.assertEqual(
            created_entries,
            Forecast.objects.all().count()
        )


class ForecastFetcherParserTests(MockedSMHIFetcherBase):
    def test_fetcher_should_be_able_to_create_a_list_of_understandable_data(self):
        should_be_there = (
            't',
            'tcc',
            'lcc',
            'mcc',
            'hcc',
            'tstm',
            'r',
            'vis',
            'gust',
            'pit',
            'pis',
            'pcat',
            'msl',
            'wd',
            'ws',

            'valid_time',
            'reference_time',
        )

        for data in self.fetcher.get_transformed_result():
            for param in should_be_there:
                self.assertTrue(
                    data.get(param, None) is not None,
                    "Parameter '" + param + "' was empty"
                )


class OverwriteOlderTests(MockedSMHIFetcherBase):
    def test_new_forecast_should_overwrite_older(self):
        self.run_create_entries()
        self.run_create_entries("2.json")

        forecast_instance = Forecast.objects.get(
            valid_time=self.fetcher.parse_time("2017-01-11T15:00:00Z")
        )

        self.assertEqual(
            forecast_instance.pit,
            1.5,
            "Forecast was NOT updated."
        )



