from rest_framework import serializers
from forecast.models import Forecast


class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = (
            'valid_time',
            'reference_time',
            't',
            'pit',
            'pcat',
            'wd',
            'ws',
            'tcc'
        )


