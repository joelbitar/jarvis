from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from forecast.models import Forecast
from forecast.serializers import ForecastSerializer


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