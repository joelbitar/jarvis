from datetime import timedelta

from django.utils import timezone

from rest_framework import viewsets
from rest_framework import generics
from sensor.models import Sensor
from sensor.models import SensorLog
from sensor.models import SensorHourly
from sensor.models import SensorDaily

from rest_framework.response import Response
from rest_framework import filters

from sensor.serializers import SensorSerializer
from sensor.serializers import SensorLogSerializer
from sensor.serializers import SensorDailySerializer
from sensor.serializers import SensorHourlySerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.filter(active=True)
    serializer_class = SensorSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name', 'id',)
    ordering = ('name',)


class SensorLogView(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        return Response(
            SensorLogSerializer(SensorLog.objects.all()[:10], many=True).data
        )


class SensorHistoryBaseView(generics.ListAPIView):
    @property
    def hours(self):
        hours = self.request.GET.get('hours')

        if hours is None:
            return None

        return int(hours)


    @property
    def days(self):
        days = self.request.GET.get('days')

        if days is None:
            return None

        return int(days)

    def get_serializer_class(self):
        if self.hours is not None:
            return SensorHourlySerializer

        if self.days is not None:
            return SensorDailySerializer

    @property
    def mean_cls(self):
        if self.days is not None:
            return SensorDaily

        if self.hours is not None:
            return SensorHourly

    @property
    def filter_kwargs(self):
        kwargs = {}

        if self.hours is not None:
            kwargs['date_time__gte'] = timezone.now() - timedelta(hours=self.hours or 12)

        if self.days is not None:
            kwargs['date__gte'] = timezone.now() - timedelta(days=self.days or 1)

        if self.kwargs.get('sensor_pk', None) is not None:
            kwargs['sensor'] = self.kwargs.get('sensor_pk')

        return kwargs

    def get_queryset(self):
        return self.mean_cls.objects.filter(
            **self.filter_kwargs
        )


class SensorsHistoryView(SensorHistoryBaseView):
    pass


class SensorHistoryView(SensorHistoryBaseView):
    pass

