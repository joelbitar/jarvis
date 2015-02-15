import json
import requests
from datetime import datetime
from django.core import mail
from django.utils import timezone

from node.models import RequestLog

class CommunicatorBase(object):
    def is_in_test_mode(self):
        return hasattr(mail, 'outbox')

    def get_response(self, url, method, data=None):
        request_method = getattr(requests, method)
        response = request_method(url, data=data)

        try:
            response_json = response.json()
        except ValueError as error:
            response_json = {
                'error': str(error),
                'payload': response.content
            }

        return response.status_code, response_json

    def create_request_log(self, url, method, data):
        try:
            r = RequestLog(
                url=url,
                method=method,
                request_data=data
            )
            r.save()

            return r
        except Exception as exception:
            #raise exception
            return None

    def update_request_log_with_response(self, request_log_object, response_status_code, response_json):
        try:
            request_log_object.response_status_code = response_status_code
            request_log_object.response_data = json.dumps(response_json)
            request_log_object.response_received = timezone.now()
            request_log_object.save()
        except Exception as exception:
            #raise exception
            pass

    def execute_request(self, url, method, data=None):
        request_log_object = self.create_request_log(url, method, data)

        print(request_log_object)

        status_code, response_json = self.get_response(url, method, data)
        self.update_request_log_with_response(
            request_log_object=request_log_object,
            response_status_code=status_code,
            response_json=response_json,
        )

        if status_code not in [200, 201]:
            return None

        return response_json


class NodeCommunicator(CommunicatorBase):
    __node = None

    def __init__(self, node):
        self.__node = node

    @property
    def node(self):
        return self.__node

    @property
    def node_url(self):
        return self.node.address

    def build_url(self, path):
        return '{node_url}/{path}'.format(
            node_url=self.node_url,
            path=path
        )

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

    def serialize_device(self):
        return {
            'name': self.device.name,
            'protocol': self.device.protocol_string,
            'description': self.device.description,
            'model': self.device.model_string,
            'controller': self.device.controller,
            'devices': self.device.devices,
            'house': self.device.house,
            'unit': self.device.unit,
            'code': self.device.code,
            'system': self.device.system,
            'units': self.device.units,
            'fade': self.device.fade,
        }

    def create(self):
        response = self.execute_request(
            self.build_url('devices/'),
            'post',
            data=self.serialize_device()
        )

        if response is None:
            return False

        self.device.node_device_pk = response['id']
        self.device.save()

        return True

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
