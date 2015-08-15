import json
try:
    import zmq
except ImportError:
    print('Could not import zmq library, this is NOT a requirement in external hubs')

import requests
from django.conf import settings
from datetime import datetime
from django.core import mail
from django.utils import timezone


from node.models import RequestLog

from node import zmqclient


class CommunicatorBase(object):
    def is_in_test_mode(self):
        if settings.TEST_MODE is not None:
            return settings.TEST_MODE

        return hasattr(mail, 'outbox')

    def get_response(self, url, method, data=None, auth_token=None):
        if not method:
            raise ValueError('Method "{method}" is not valie'.format(method=method))

        if self.is_in_test_mode():
            print('In test mode, does not execute {method} request'.format(method=method), 'to', url, 'with data:', data)
            return 200, {'fake': 'response', 'id': 666}

        request_headers = {}
        if auth_token is not None:
            request_headers['Authorization'] = 'Token ' + auth_token

        request_method = getattr(requests, method)
        try:
            request_headers['content-type'] = 'application/json'

            if method in ['post', 'put']:
                response = request_method(url, data=json.dumps(data), headers=request_headers
            )
            else:
                response = request_method(url, headers=request_headers)

        except requests.ConnectionError:
            return 503, {
                'error': 'connection_error',
                'message': 'Could not connect to node, perhaps not running?',
                'url': url
            }

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

    def execute_request(self, url, method, data=None, auth_token=None):
        request_log_object = self.create_request_log(url, method, data)

        status_code, response_json = self.get_response(url, method, data, auth_token)
        self.update_request_log_with_response(
            request_log_object=request_log_object,
            response_status_code=status_code,
            response_json=response_json,
        )

        return status_code, response_json


class NodeCommunicator(CommunicatorBase):
    __node = None

    def __init__(self, node):
        self.__node = node

    @property
    def node(self):
        return self.__node

    @property
    def node_url(self):
        return 'http://{address}:{port}'.format(
            address=self.node.address,
            port=self.node.api_port
        )

    def build_url(self, path, **kwargs):
        return '{node_url}/{path}'.format(
            node_url=self.node_url,
            path=path.format(**kwargs)
        )

    def execute_request(self, url, method, data=None, auth_token=None):
        return super(NodeCommunicator, self).execute_request(
            url=url,
            method=method,
            data=data,
            auth_token=auth_token or self.node.auth_token
        )

    def get_all_devices(self):
        pass

    def write_conf(self):
        status_code, response_json = self.execute_request(
            self.build_url('conf/write/'),
            method='post',
            data={}
        )

        if status_code not in [200]:
            return False

        self.node.device_set.all().update(
            written_to_conf_on_node=True
        )

        return True

    def restart_daemon(self):
        status_code, response_json = self.execute_request(
            self.build_url('conf/restart-daemon/'),
            method='post',
            data={}
        )

        return status_code in [200]


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

    def execute_device_command(self, command_name, command_data=None):
        data = {
            'command_name': command_name,
            'command_data': command_data or {},
            'device_id': self.device.node_device_pk
        }
        node_name = self.device.node.name

        # if node name is testnode, do not continue.
        if node_name == 'testnode':
            print('Node name is "testnode" does NOT send message', data)
            return True

        # Setting socket and context if there is none.
        try:
            if zmqclient.sockets.get(node_name, None) is None:
                print('Connecting socket ZeroMQ... ', self.device.node.address)
                zmqclient.contexts[node_name] = zmq.Context()
                zmqclient.sockets[node_name] = zmqclient.context.socket(zmq.PUB)
                zmqclient.sockets[node_name].connect("tcp://{node_adress}:5557".format(
                    self.device.node.address
                ))

                # In case this is a new socket we need to sleep.
                from time import sleep
                sleep(0.5)

        # compile and send message
            zmqclient.socket.send_string(
                'command:' + json.dumps(data)
            )
        except Exception as e:
            print(e)
            print('ERROR while trying to publish message', data)
            return False
        return True

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
        status_code, response_json = self.execute_request(
            self.build_url('devices/'),
            'post',
            data=self.serialize_device()
        )

        print(status_code, response_json)

        if status_code not in [200, 201]:
            return False

        self.device.node_device_pk = response_json['id']
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
        # If is dimmer, set dimer to 255
        if self.device.is_dimmable:
            return self.dim(255)

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
        print('Learn is ignored, is not executed')
        return True
        success = self.execute_device_command(
            'learn'
        )

        if not success:
            return False

        self.device.learnt_on_node = True
        self.device.save()

        return True

    def dim(self, dimlevel):
        success = self.execute_device_command(
            'dim',
            command_data={
                'dimlevel': dimlevel
            }
        )

        if not success:
            return False

        self.device.state = dimlevel
        self.device.save()

        return True

