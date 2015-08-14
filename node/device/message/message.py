__author__ = 'joel'
import json


class Message(object):
    __message_string = ""
    __json_obj = None

    def __init__(self, message_string=None):
        self.__message_string = message_string
        self.__json_obj = None

    @property
    def message_string(self):
        return self.__message_string

    @property
    def message_obj(self):
        if self.__json_obj is not None:
            return self.__json_obj

        self.decode()

        return self.__json_obj

    def decode(self):
        self.__json_obj = json.loads(self.__message_string)

    def to_json(self):
        raise NotImplementedError('Need to implement "to_json" on object')

    def encode(self):
        self.__message_string = json.dumps(self.to_json())
