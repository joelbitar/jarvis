import json
import re

from time import strptime
from time import mktime
import datetime
from datetime import timedelta

from django.db.models import Avg
from django.db.models import Sum
from django.db.models import Min
from django.db.models import Max

from django.db.models import QuerySet

from django.utils import timezone
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from forecast.models import Forecast
from forecast.serializers import ForecastSerializer


class NowForecastView(viewsets.generics.ListAPIView):
    serializer_class = ForecastSerializer

    def serialize_forecast_queryset(self, queryset):
        return self.get_serializer(
            instance=queryset,
            many=True
        ).data

    def serialize_forecasts(self, *args):
        output = []
        for queryset in args:
            if isinstance(queryset, QuerySet):
                output.append(
                    self.serialize_forecast_queryset(
                        queryset
                    )
                )
            else:
                output.append(
                    queryset
                )

        return output

    def get_grouped_forecasts(self, group_span, start, count):
        """
        :param group_span: how many hours each group should span over
        :param start:  when to start
        :param count:  how many groups
        :return: list

        If we send group span 2, start now and count 3, we will get a six hour period in three groups
        """

        grouped = []
        runs = 0

        while len(grouped) < count:
            valid_time_from = start + timedelta(hours=runs * group_span)

            grouped_forecasts = Forecast.objects.filter(
                valid_time__gte=valid_time_from,
                valid_time__lt=start + timedelta(hours=(runs + 1) * group_span)
            ).aggregate(
                Avg('t'), Avg('tcc'), Avg('tstm'), Avg('r'), Avg('gust'), Avg('pcat'), Avg('ws'), Avg('wd'), Sum('pit'), Sum('pis'), Min('valid_time'), Max('valid_time')
            )

            group = {
                'span': group_span
            }

            for key, value in grouped_forecasts.items():
                key = re.sub('(__((avg)|(sum)))', '', key)

                if value is not None:
                    if key in ('t', 'msl', 'vis', 'ws', 'gust', 'pis', 'pit', ):
                        value = round(value, 1)

                    if key in ('wd', 'r', 'tstm', 'tcc', 'lcc', 'mcc', 'hcc', 'pcat', ):
                        value = round(value)

                group[key] = value

            grouped.append(
                group
            )

            runs += 1

        return grouped

    def get_forecast(self, date):
        return Response(
            self.serialize_forecasts(
                Forecast.objects.filter(
                    valid_time__gte=date
                )[:12],
                self.get_grouped_forecasts(
                    3, date + timedelta(hours=12), 12
                ),
            )
        )


    def get(self, request, date=None, *args, **kwargs):
        if date is None:
            date = timezone.now()
        else:
            date = timezone.make_aware(
                datetime.datetime.fromtimestamp(mktime(strptime(date, "%Y-%m-%dT%H:%M:%S")))
            )

        return self.get_forecast(date=date)


class ShortForecastView(NowForecastView):
    def get_forecast(self, date):
        return Response(
            self.serialize_forecasts(
                Forecast.objects.filter(
                    valid_time__gte=date
                )[:6],
                self.get_grouped_forecasts(
                    3, date + timedelta(hours=5), 6
                )
            )
        )


class LatestForecastView(viewsets.generics.ListAPIView):
    serializer_class = ForecastSerializer

    def get(self, request, *args, **kwargs):
        return Response(
            self.get_serializer(
                instance=Forecast.objects.all().order_by(
                    'valid_time'
                )[:71],
                many=True
            ).data
        )


class ForecastViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Forecast.objects.all().order_by(
            'valid_time'
        )

    serializer_class = ForecastSerializer