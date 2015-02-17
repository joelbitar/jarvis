import json

from django.test import TestCase
from device.models import Device
from device.models import Group
from node.models import Node
from node.models import RequestLog

from node.communicator import NodeDeviceCommunicator


class DeviceModelTestsBase(TestCase):
    def setUp(self):
        n = Node()
        n.address = 'address'
        n.name = 'Test Node'
        n.save()

        d = Device()
        d.name = 'TestDevice'
        d.protocol = Device.PROTOCOL_ARCHTEC
        d.model = Device.MODEL_CODESWITCH
        d.node = n
        d.save()

        g = Group()
        g.name = 'Group'
        g.save()
        g.devices.add(d)
        g.save()

        self.node = n
        self.device = d
        self.group = g

    def refresh(self, obj):
        return obj.__class__.objects.get(pk=obj.pk)


class DeviceTest(DeviceModelTestsBase):
    def test_devices_have_been_created(self):
        self.assertEqual(1, self.device.group_set.all().count())


class NodeCrudCommunicationTests(DeviceModelTestsBase):
    def test_create_device_on_node_rest_call(self):
        nd = NodeDeviceCommunicator(device=self.device)

        def fake_get_response(url, method, data):
            return 201, {
                'id' : 1001
            }

        nd.get_response = fake_get_response
        self.assertTrue(nd.create())
        self.assertEqual(self.refresh(self.device).node_device_pk, 1001)

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            self.node.address + '/devices/'
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertJSONEqual(
            r.response_data,
            json.dumps({'id': 1001})
        )

        self.assertEqual(
            r.method,
            'post'
        )

        self.assertEqual(
            r.response_status_code,
            201
        )

    def test_should_not_be_able_to_execute_requests_on_device_that_has_no_node_id(self):
        nd = NodeDeviceCommunicator(device=self.device)

        self.assertRaises(
            ValueError,
            nd.update
        )

        self.assertRaises(
            ValueError,
            nd.delete
        )

    def test_delete_device_on_node_rest_call(self):
        nd = NodeDeviceCommunicator(device=self.device)

        def fake_get_response(url, method, data):
            return 200, {}

        nd.get_response = fake_get_response

        self.device.node_device_pk = 1001
        self.device.save()

        self.assertTrue(nd.delete())

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            self.node.address + '/devices/{node_device_pk}/'.format(node_device_pk=self.device.node_device_pk)
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertJSONEqual(
            r.response_data,
            json.dumps({})
        )

        self.assertEqual(
            r.method,
            'delete'
        )

        self.assertEqual(
            r.response_status_code,
            200
        )

    def test_update_device_on_node_rest_call(self):
        nd = NodeDeviceCommunicator(device=self.device)

        def fake_get_response(url, method, data):
            return 200, {}

        nd.get_response = fake_get_response

        self.device.node_device_pk = 1001
        self.device.save()

        self.assertTrue(nd.update())

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            self.node.address + '/devices/{node_device_pk}/'.format(node_device_pk=self.device.node_device_pk)
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertJSONEqual(
            r.response_data,
            json.dumps({})
        )

        self.assertEqual(
            r.method,
            'put'
        )

        self.assertEqual(
            r.response_status_code,
            200
        )


class NodeControlCommunicationsTests(DeviceModelTestsBase):
    def setUp(self):
        super(NodeControlCommunicationsTests, self).setUp()

        self.device.node_device_pk = 1001
        self.device.save()

    def test_send_learn_command(self):
        nd = NodeDeviceCommunicator(device=self.device)

        def fake_get_response(url, method, data):
            if data != {'command': 'learn'}:
                print(data)
                raise ValueError()
            return 200, {}

        nd.get_response = fake_get_response
        self.assertTrue(nd.learn())

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            self.node.address + '/devices/{node_device_pk}/command/'.format(node_device_pk=self.device.node_device_pk)
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertEqual(
            r.response_status_code,
            200
        )

    def test_send_off_command(self):
        nd = NodeDeviceCommunicator(device=self.device)

        def fake_get_response(url, method, data):
            if data != {'command': 'off'}:
                raise ValueError()
            return 200, {}

        nd.get_response = fake_get_response
        self.assertTrue(nd.turn_off())

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            self.node.address + '/devices/{node_device_pk}/command/'.format(node_device_pk=self.device.node_device_pk)
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertEqual(
            r.response_status_code,
            200
        )

    def test_send_on_command(self):
        nd = NodeDeviceCommunicator(device=self.device)

        def fake_get_response(url, method, data):
            if data != {'command': 'on'}:
                print(data)
                raise ValueError()
            return 200, {}

        nd.get_response = fake_get_response
        self.assertTrue(nd.turn_on())

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            self.node.address + '/devices/{node_device_pk}/command/'.format(node_device_pk=self.device.node_device_pk)
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertEqual(
            r.response_status_code,
            200
        )

