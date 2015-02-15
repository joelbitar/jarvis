import requests
from django.core import mail


class CommunicatorBase(object):
    def is_in_test_mode(self):
        return hasattr(mail, 'outbox')

    def get_response(self, url, method, data=None):
        response = requests.get(url)


class NodeCommunicator(CommunicatorBase):
    __node = None

    def __init__(self, node):
        self.__node = node

    @property
    def node(self):
        return self.__node

    def get_all_devices(self):
        pass


class NodeDeviceCommunicator(NodeCommunicator):
    __device = None

    def __init__(self, device):
        self.__device = device
        super(NodeDeviceCommunicator, self).__init__(node=device.node)

    @property
    def device(self):
        return self.__device

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
