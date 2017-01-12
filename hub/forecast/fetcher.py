from time import mktime
from time import strptime
import requests
import json
import datetime
from django.utils import timezone
import pytz

from forecast.models import Forecast


class ForecastFetcher(object):
    def get_url(self):
        url = "http://opendata-download-metfcst.smhi.se/api/category/pmp2g/version/2/geotype/point/lon/12.476692/lat/57.892365/data.json"

        return url

    def get_parsed_result(self):
        return json.loads(
            self.fetch_from_shmi()
        )

    def fetch_from_shmi(self):
        response = requests.get(
            self.get_url()
        )

        return response.content.decode('utf-8')

    def parse_time(self, time_string):
        return timezone.make_aware(
            datetime.datetime.fromtimestamp(mktime(strptime(time_string, "%Y-%m-%dT%H:%M:%SZ"))),
            pytz.timezone('GMT')
        )

    def create_entry(self, data):
        # Check if a forecast with this valid time exists

        try:
            forecast = Forecast.objects.get(
                valid_time=data['valid_time']
            )

            for key, value in data.items():
                # Ignore the following attributes
                if key in ('valid_time',):
                    continue

                setattr(forecast, key, value)

        except Forecast.DoesNotExist:
            forecast = Forecast(
                **data
            )

        # Save it!
        forecast.save()

        return forecast

    def transform_data(self, data, **kwargs):
        result = {}

        parameters = (
            ('t',       't'),
            ('tcc',     'tcc_mean'),
            ('lcc',     'lcc_mean'),
            ('mcc',     'mcc_mean'),
            ('hcc',     'hcc_mean'),
            ('tstm',    'tstm'),
            ('r',       'r'),
            ('vis',     'vis'),
            ('gust',    'gust'),
            ('pit',     'pmean'),
            ('pis',     'pmean'),
            ('pcat',    'pcat'),
            ('msl',     'msl'),
            ('wd',      'wd'),
            ('ws',      'ws'),
        )

        for result_key, parameter_conf in parameters:
            for entry in data['parameters']:
                if entry['name'] == parameter_conf:
                    values = entry['values']
                    result[result_key] = values[0]
                    break

        result['valid_time'] = self.parse_time(data['validTime'])
        result['reference_time'] = self.parse_time(kwargs['reference_time'])

        return result

    def get_transformed_result(self):
        result = self.get_parsed_result()

        for data in result['timeSeries']:
            yield self.transform_data(
                data=data,
                reference_time=result['referenceTime']
            )

        return

    def create_entries(self):
        for data in self.get_transformed_result():
            yield self.create_entry(
                data
            )





