from django.test import TestCase
from device.models import Device
from device.models import Group
from node.models import Node

from node.communicator import NodeDeviceCommunicator

# Create your tests here.

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

class DeviceTest(DeviceModelTestsBase):
    def test_devices_have_been_created(self):
        self.assertEqual(1, self.device.group_set.all().count())

class NodeCrudCommunicationTests(DeviceModelTestsBase):
    def test_create_device_on_node_rest_call(self):
        nd = NodeDeviceCommunicator(device=self.device)
        self.assertTrue(nd.create())

    def test_delete_device_on_node_rest_call(self):
        self.assertTrue(False)

    def test_update_device_on_node_rest_call(self):
        self.assertTrue(False)


class NodeControlCommunicationsTests(DeviceModelTestsBase):
    def test_send_learn_command(self):
        self.assertTrue(False)

    def test_send_off_command(self):
        self.assertTrue(False)

    def test_send_on_command(self):
        self.assertTrue(False)

