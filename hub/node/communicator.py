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
        if self.is_in_test_mode():
            print('In test mode, does not execute {method} request'.format(method=method), 'to', url, 'with data:', data)
            return 200, {'fake': 'request'}

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

    def build_url(self, path, **kwargs):
        return '{node_url}/{path}'.format(
            node_url=self.node_url,
            path=path.format(**kwargs)
        )

    def get_all_devices(self):
        pass

    def write_conf(self):
        response = self.execute_request(
            self.build_url('conf/write/'),
            method='post',
            data={}
        )

        if response == None:
            return False

        self.node.device_set.all().update(
            written_to_conf_on_node=True
        )

        return True

    def restart_daemon(self):
        response = self.execute_request(
            self.build_url('conf/restart-daemon/'),
            method='post',
            data={}
        )

        return response is not None


class NodeDeviceCommunicator(NodeCommunicator):
    __device = None

    def __init__(self, device):
        self.__device = device
        super(NodeDeviceCommunicator, self).__init__(node=device.node)

    @property
    def device(self):
        return self.__device

    def get_device_url(self):
        if self.device.node_device_pk is None:
            raise ValueError('Could not build URL with device that has no node_pk')

        return self.build_url(
            'devices/{node_device_pk}/'.format(
                node_device_pk=self.device.node_device_pk
            )
        )

    def get_device_command_url(self):
        return self.get_device_url() + 'command/'

    def execute_device_command(self, command_name, command_data=None):
        data = {
            'command': command_name,
        }

        # Setting the 'data' key in request data to include all command data
        if command_data is not None:
            data['data'] = command_data

        response = self.execute_request(
            self.get_device_command_url(),
            method='post',
            data=data
        )

        return response is not None


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
        response = self.execute_request(
            url=self.get_device_url(),
            method='delete',
        )

        return response is not None

    def update(self):
        response = self.execute_request(
            url=self.get_device_url(),
            method='put',
            data=self.serialize_device(),
        )

        return response is not None

    def turn_on(self):
        success = self.execute_device_command(
            'on'
        )

        if not success:
            return False

        self.device.state = 1
        self.device.save()

        return True

    def turn_off(self):
        success = self.execute_device_command(
            'off'
        )

        if not success:
            return False

        self.device.state = 0
        self.device.save()

        return True


    def learn(self):
        success = self.execute_device_command(
            'learn'
        )

        if not success:
            return False

        self.device.learnt_on_node = True
        self.device.save()

        return True
