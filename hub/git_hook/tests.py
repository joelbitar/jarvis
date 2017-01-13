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

    def get_hook_response(self, ref=None, **kwargs):
        response = self.client.post(
            reverse("git_hook"),
            data=json.dumps(
                {
                    "ref": ref or "refs/heads/master"
                }
            ),
            content_type='application/json',
            **kwargs
        )

        return response


# Create your tests here.
class GitHookAuthTests(GitHubHookTestsBase):
    def setUp(self):
        self.client = Client()

    def test_should_get_not_auhtorized_when_posting_without_secret(self):
        response = self.get_hook_response()

        self.assertEqual(
            response.status_code,
            403
        )

    def test_should_get_not_auhtorized_when_posting_with_wrong_secret(self):
        kwargs = {
            "X-Hub-Signature": "wrong key"
        }

        response = self.get_hook_response(
            **kwargs
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_should_get_ok_when_posting_with_secret(self):
        kwargs = {
            "X-Hub-Signature":settings.GITHUB_WEBHOOK_SECRET
        }

        response = self.get_hook_response(
            **kwargs
        )

        self.assertEqual(
            response.status_code,
            202
        )

    def test_should_get_ok_when_posting_with_weirdly_cased_secret(self):
        kwargs = {
            "X-Hub-Signature":settings.GITHUB_WEBHOOK_SECRET
        }

        response = self.get_hook_response(
            **kwargs
        )

        self.assertEqual(
            response.status_code,
            202
        )

    def test_should_return_does_not_match(self):
        kwargs = {
            "X-Hub-Signature":"not_correct_secret"
        }

        response = self.get_hook_response(
            **kwargs
        )

        self.assertEqual(
            json.loads(response.content.decode('utf-8')).get('detail'),
            'Signature did not match'
        )

    def test_should_return_could_not_find(self):
        response = self.get_hook_response()

        self.assertEqual(
            json.loads(response.content.decode('utf-8')).get('detail'),
            'Could not find signature'
        )




class GitHubHookAuthTestsWithBaseClass(GitHubHookTestsBase):
    def test_should_get_ok_when_using_default_headers(self):
        response = self.get_hook_response()

        self.assertEqual(
            response.status_code,
            202
        )


class GitHubNodeTests(GitHubHookTestsBase):
    def setUp(self):
        super(GitHubNodeTests, self).setUp()

        self.node = Node.objects.create(
            name='TestNode',
            address='example.com',
            auth_token='asefasefasefasef',
            api_port=8001
        )

    def test_should_call_to_nodes_run_git_hooks(self):
        response = self.get_hook_response()

        self.assertEqual(
            response.status_code,
            202
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
            return 202, {}

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
        old_hub_url = settings.MAIN_HUB_URL
        settings.MAIN_HUB_URL = 'http://example.com/nothihng/'

        response = self.get_hook_response()

        self.assertEqual(
            response.status_code,
            202
        )

        settings.MAIN_HUB_URL = old_hub_url


class GitHookTestWebhookPayloads(GitHubHookTestsBase):
    def test_should_not_execute_if_ref_is_not_master(self):
        response = self.get_hook_response(
            ref="refs/heads/changes"
        )

        self.assertEqual(
            response.status_code,
            400
        )
