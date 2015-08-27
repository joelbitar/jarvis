from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from event.receiver import Receiver
from event.models import Signal

from event.serializers import RecentSignalSerializer


class RecentSignalsView(viewsets.generics.ListAPIView):
    queryset = Signal.objects.all()
    serializer_class = RecentSignalSerializer

    def get(self, request, *args, **kwargs):
        return Response(
            self.get_serializer(
                instance=self.queryset[:50],
                many=True
            ).data
        )


class EventReceiverView(APIView):
    permission_classes = ()

    def post(self, request):
        raw_event_string = request.data.get('raw')

        if raw_event_string is None:
            return Response(status=400)

        receiver = Receiver()
        signal, unit = receiver.act_on_raw_event_string(raw_event_string)

        return Response()

