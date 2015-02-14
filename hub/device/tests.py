from django.test import TestCase
from device.models import Device
from device.models import Group
from node.models import Node

# Create your tests here.

class ModelTests(TestCase):
    def test_create_device(self):
        n = Node()
        n.hostname = 'test'
        n.ip = '127.0.0.1'
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


