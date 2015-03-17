import requests
import json

from forecast.models import Forecast


class ForecastFetcher(object):
    def get_url(self):
        url = "http://opendata-download-metfcst.smhi.se/api/category/pmp1.5g/version/1/geopoint/lat/57.892365/lon/12.476692/data.json"

        return url

    def get_parsed_result(self):
        result = self.fetch_from_shmi()
        return json.loads(
            result
        )

    def fetch_from_shmi(self):
        url = self.get_url()

        response = requests.get(
            url
        )

        return response.content.decode('utf-8')

    def create_entry(self, data):
        # Check if a forecast with this valid time exists
        try:
            forecast = Forecast.objects.get(
                valid_time=data['valid_time']
            )
        except Forecast.DoesNotExist:
            forecast = Forecast(
                **data
            )

        forecast.save()

        return forecast

    def transform_data(self, data, **kwargs):
        map = (
            ('validTime', 'valid_time'),
        )

        for key_from, key_to in map:
            data[key_to] = data[key_from]
            del data[key_from]

        data.update(
            kwargs
        )

        return data

    def create_entries(self):
        result = self.get_parsed_result()

        for data in result['timeseries']:
            entry = self.create_entry(
                self.transform_data(
                    data=data,
                    reference_time=result['referenceTime']
                )
            )




