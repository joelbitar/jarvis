import json


class Base(object):
    property_map = None

    def __init__(self, request):
        self.request = request

    def get_json(self):
        return json.loads(self.request.body.decode('utf-8'))

    def parse(self):
        raise NotImplementedError()
