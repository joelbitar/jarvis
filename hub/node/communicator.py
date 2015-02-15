import requests
from django.core import mail

class SenderBase(object):
    def is_in_test_mode(self):
        return hasattr(mail, 'outbox')

    def get_response(self, url, method, data=None):
        response = requests.get(url)

class NodeRestSender(SenderBase):
    __node = None 
    def __init__(self, node):
        self.__node = node

    @property
    def node(self):
        return self.__node

    def get_all_devices(self):
        pass

class NodeDeviceRestSender(SenderBase):
    __device = None
    def __init__(self, device):
        self.__device = device

    @property
    def device(self):
        return self.__device

    @property
    def node(self):
        return self.device.node


class NodeDevice(NodeDeviceRestSender):
    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    def learn(self):
        pass
