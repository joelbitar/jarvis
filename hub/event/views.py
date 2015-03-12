from rest_framework.views import APIView
from rest_framework.response import Response

from event.receiver import Receiver


class EventReceiverView(APIView):
    permission_classes = ()

    def post(self, request):
        raw_event_string = request.data.get('raw')

        if raw_event_string is None:
            return Response(status=400)

        receiver = Receiver()
        signal, unit = receiver.act_on_raw_event_string(raw_event_string)

        return Response()

