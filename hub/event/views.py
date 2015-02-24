from rest_framework.views import APIView
from rest_framework.response import Response

from event.receiver import Receiver


# Create your views here.
class EventReceiverView(APIView):
    def post(self, request):
        raw_event_string = request.data.get('raw')

        if raw_event_string is None:
            return Response(status=400)

        receiver = Receiver()

        receiver.parse_raw_event(raw_event_string)

        return Response()

