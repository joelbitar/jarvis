import json
from django.core.urlresolvers import reverse

from django.test import TestCase
from node.communicator import NodeCommunicator
from node.models import Node
from django.contrib.auth.models import User
from device.models import Device
from node.models import RequestLog
from django.test.client import Client


class NodeAdminTests(TestCase):
    def setUp(self):
        self.node = Node(
            name='TestNode'
        )

        self.node.save()

        self.user = User.objects.create_user(
            username='test',
            password='test'
        )

        self.logged_in_client = Client()
        self.logged_in_client.login(
            username='test',
            password='test'
        )

    def test_should_get_all_nodes(self):
        response = self.logged_in_client.get(
            reverse('node-list')
        )

        self.assertTrue(
            reverse('node-list').startswith('/api/'),
            'Tests that the prefix for all APIs is api/ ' + reverse('node-list')
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(json.loads(response.content.decode('utf-8'))), Node.objects.all().count())

    def test_should_send_write_conf_command_with_ajax_to_hub(self):
        response = self.logged_in_client.get(reverse('node-writeconf', kwargs={'pk' : self.node.pk}))

        self.assertEqual(response.status_code, 200)

    def test_should_mark_all_node_devices_as_written_to_conf(self):
        for i in range(2):
            d = Device(
                node=self.node,
                protocol=Device.PROTOCOL_ARCHTEC,
                model=Device.MODEL_SELFLEARNING_SWITCH
            )
            d.save()

        response = self.logged_in_client.get(reverse('node-writeconf', kwargs={'pk' : self.node.pk}))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            2,
            Device.objects.all().count()
        )

        self.assertEqual(
            2,
            self.node.device_set.all().count()
        )

        self.assertEqual(
            0,
            Device.objects.filter(written_to_conf_on_node=False).count(),
        )

        self.assertEqual(
            2,
            Device.objects.all().filter(written_to_conf_on_node=True).count()
        )

    def test_should_send_restart_command_with_ajax_to_hub(self):
        response = self.logged_in_client.get(reverse('node-restartdaemon', kwargs={'pk' : self.node.pk}))

        self.assertEqual(response.status_code, 200)

    def test_should_send_write_conf_command_and_receive_a_ok(self):
        c = NodeCommunicator(node=self.node)

        def fake_get_response(url, method, data):
            return 200, {}

        c.get_response = fake_get_response

        response = c.write_conf()

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            self.node.address + '/conf/write/'
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertEqual(
            r.response_status_code,
            200
        )

    def test_should_send_restart_daemon_command_and_receive_a_ok(self):
        c = NodeCommunicator(node=self.node)

        def fake_get_response(url, method, data):
            return 200, {}

        c.get_response = fake_get_response

        response = c.restart_daemon()

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            self.node.address + '/conf/restart-daemon/'
        )

        self.assertIsNotNone(
            r.response_data,
        )

        self.assertEqual(
            r.response_status_code,
            200
        )
