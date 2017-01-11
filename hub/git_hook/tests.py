from django.conf import settings
from django.core.urlresolvers import reverse

import json

from node.communicator import NodeCommunicator

from node.models import Node
from node.models import RequestLog

from django.test import TestCase
from django.test import Client


class GitHubHookTestsBase(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.defaults["X-Hub-Signature"] = settings.GITHUB_WEBHOOK_SECRET


# Create your tests here.
class GitHookAuthTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_should_get_not_auhtorized_when_posting_without_secret(self):
        response = self.client.post(
            reverse("git_hook")
        )

        self.assertEqual(
            response.status_code,
            404
        )

    def test_should_get_not_auhtorized_when_posting_with_wrong_secret(self):
        kwargs = {
            "X-Hub-Signature": "wrong key"
        }

        response = self.client.post(
            reverse("git_hook"),
            **kwargs
        )

        self.assertEqual(
            response.status_code,
            404
        )

    def test_should_get_ok_when_posting_with_secret(self):
        kwargs = {
            "X-Hub-Signature":settings.GITHUB_WEBHOOK_SECRET
        }

        response = self.client.post(
            reverse("git_hook"),
            **kwargs
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_should_get_ok_when_posting_with_weirdly_cased_secret(self):
        kwargs = {
            "X-Hub-Signature":settings.GITHUB_WEBHOOK_SECRET
        }
        response = self.client.post(
            reverse("git_hook"),
            **kwargs
        )

        self.assertEqual(
            response.status_code,
            200
        )


class GitHubHookAuthTestsWithBaseClass(GitHubHookTestsBase):
    def test_should_get_ok_when_using_default_headers(self):
        response = self.client.post(
            reverse("git_hook")
        )

        self.assertEqual(
            response.status_code,
            200
        )


class GitHubNodeTests(GitHubHookTestsBase):
    def setUp(self):
        super(GitHubNodeTests, self).setUp()

        self.node = Node.objects.create(
            name='TestNode',
            address='http://example.com',
            auth_token='asefasefasefasef',
            api_port=8001
        )

    def test_should_call_to_nodes_run_git_hooks(self):
        response = self.client.post(
            reverse("git_hook")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            RequestLog.objects.all().count(),
            1
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            'http://' + self.node.address + ':' + str(self.node.api_port) + '/githook/hook/'
        )

    def test_should_execute_to_correct_response(self):
        c = NodeCommunicator(node=self.node)

        def fake_get_response(url, method, data, auth_token):
            return 200, {}

        c.get_response = fake_get_response

        c.upgrade_node()

        self.assertEqual(
            1,
            RequestLog.objects.all().count()
        )

        r = RequestLog.objects.get(pk=1)
        self.assertEqual(
            r.url,
            'http://' + self.node.address + ':' + str(self.node.api_port) + '/githook/hook/'
        )

    def test_should_request_on_main_hub(self):
        settings.TEST_MODE = False
        old_hub_url = settings.MAIN_HUB_URL

        settings.MAIN_HUB_URL = 'http://127.0.0.1:9090/nothihng/'

        response = self.client.post(
            reverse("git_hook")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        settings.MAIN_HUB_URL = old_hub_url
        settings.TEST_MODE = True
