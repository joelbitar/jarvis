import os
import json

from django.conf import settings

from django.core.urlresolvers import reverse

from forecast import fetcher
from django.test import TestCase

from forecast.models import Forecast

from device.tests import HasLoggedInClientBase


class MockedSMHIFetcherBase(HasLoggedInClientBase):
    FAKE_RESPONSE_JSON_FILE_NAME = '1.json'

    def setUp(self):
        super(MockedSMHIFetcherBase, self).setUp()

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


class FetchFromSMHITests(MockedSMHIFetcherBase):
    def test_create_entries_should_produce_equal_number_of_units_as_there_is_timeseries(self):
        json = self.fetcher.get_parsed_result()

        self.fetcher.create_entries()

        self.assertEqual(
            Forecast.objects.all().count(),
            len(json['timeseries'])
        )

    def test_create_entries_should_not_yield_duplicates(self):
        self.fetcher.create_entries()
        created_entries = Forecast.objects.all().count()
        self.fetcher.create_entries()

        self.assertEqual(
            created_entries,
            Forecast.objects.all().count()
        )


class ForecastAPITests(MockedSMHIFetcherBase):
    def setUp(self):
        super(ForecastAPITests, self).setUp()

        self.fetcher.create_entries()

    def test_should_return_seventy_one_entries_even_if_there_are_more(self):
        self.FAKE_RESPONSE_JSON_FILE_NAME = '2.json'
        self.fetcher.create_entries()

        r = self.logged_in_client.get(
            reverse('latest-forecast')
        )

        self.assertEqual(
            71,
            len(
                json.loads(
                    r.content.decode('utf-8')
                )
            )
        )

    def test_should_render_fields_in_forecasts(self):
        r = self.logged_in_client.get(
            reverse('forecasts-detail', kwargs={
                'pk': 1
            })
        )

        j = json.loads(
            r.content.decode('utf-8')
        )

        should_have_keys = (
            'valid_time',
            'reference_time',
            't',
            'pit',
            'pcat',
            'wd',
            'ws',
            'tcc'
        )

        for should_have_key in should_have_keys:
            self.assertTrue(
                should_have_key in j.keys()
            )

        self.assertEqual(
            len(should_have_keys),
            len(j.keys()),
            'Does not match number of items in response: ' + ", ".join(j.keys())
        )



