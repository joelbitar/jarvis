import json


class Base(object):
    property_map = None

    def __init__(self, request):
        self.request = request

    def get_json(self):
        return json.loads(self.request.body.decode('utf-8'))

    def parse(self):
        raise NotImplementedError()


class ResponseBase(object):
    def __init__(self, speak_text=None, display_text=None, data=None, extra=None):
        self.__speak_text = speak_text
        self.__display_text = display_text
        self.__data = data
        self.__extra = extra or {}

    @property
    def speak_text(self):
        return self.__speak_text

    @speak_text.setter
    def speak_text(self, property):
        self.__speak_text = property

    @property
    def display_text(self):
        return self.__display_text or self.speak_text

    @display_text.setter
    def display_text(self, property):
        self.__display_text = property

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, property):
        self.__data = property

    @property
    def extra(self):
        return self.__extra

    def set_extra(self, key, value):
        self.__speak_text[key] = value

    def get_dict(self):
        raise NotImplementedError()
