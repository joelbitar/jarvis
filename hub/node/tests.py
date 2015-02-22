import json
from django.core.urlresolvers import reverse

from django.test import TestCase
from node.communicator import NodeCommunicator
from node.models import Node
from node.models import RequestLog
from django.test.client import Client


class NodeAdminTests(TestCase):
    def setUp(self):
        self.node = Node(
            name='TestNode'
        )

        self.node.save()

    def test_should_get_all_nodes(self):
        client = Client()

        response = client.get('/nodes/')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(json.loads(response.content.decode('utf-8'))), Node.objects.all().count())

    def test_should_send_write_conf_command_with_ajax_to_hub(self):
        client = Client()

        response = client.get(reverse('node_writeconf', kwargs={'pk' : self.node.pk}))

        self.assertEqual(response.status_code, 200)

    def test_should_send_restart_command_with_ajax_to_hub(self):
        client = Client()

        response = client.get(reverse('node_restartdaemon', kwargs={'pk' : self.node.pk}))

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
