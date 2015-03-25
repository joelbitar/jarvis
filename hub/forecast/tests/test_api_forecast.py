__author__ = 'joel'
import json
from forecast.models import Forecast

from django.test import TestCase
from device.tests import HasLoggedInClientBase
from forecast.tests.test_fetcher import MockedSMHIFetcherBase


class TestForecastNowApi(MockedSMHIFetcherBase):
    def setUp(self):
        super(TestForecastNowApi, self).setUp()
        self.fetcher.create_entries()

    def test_should_have_correct_basic_structure_in_now_call(self):
        for f in Forecast.objects.all():
            print(f.valid_time)

        r = self.get_json_response(
            'forecast-now',
            kwargs={
                'date': '2015-03-15T15:00:00'
            }
        )

        self.assertIsInstance(
            r,
            list
        )

        print('RESPONSE')
        print(r)
        for v in r:
            print('-'*55)
            for l in v:
                if 'valid_time' in  l.keys():
                    print(l['valid_time'])
                else:
                    print(l['valid_time__min'], l['valid_time__max'])
                print(l)

        self.assertEqual(
            len(r),
            3
        )

        for item in r:
            self.assertTrue(
                len(item) > 0,
                'Should not be empty'
            )


